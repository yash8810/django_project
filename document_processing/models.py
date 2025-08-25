import os
import re
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField

def validate_username(value):
    """Validate that username contains exactly two words."""
    if len(value.strip().split()) != 2:
        raise ValidationError("Username must be two words separated by a space.")

def validate_email(value):
    """Validate email domain."""
    if not value.endswith("@gmail.com"):
        raise ValidationError("Email must be a @gmail.com address.")

def validate_password(value):
    """Validate password complexity."""
    if (len(value) < 8 or
        not re.search(r"\d", value) or
        not re.search(r"[A-Z]", value) or
        not re.search(r"[a-z]", value) or
        not re.search(r"[!@#$%^&*()_+=]", value)):
        raise ValidationError(
            "Password must be at least 8 characters with a number, special character, uppercase and lowercase letter."
        )

# class CustomUser(AbstractUser):
#     username = models.CharField(
#         max_length=150,
#         unique=True,
#         validators=[validate_username]
#     )
#     email = models.EmailField(
#         unique=True,
#         validators=[validate_email]
#     )
#     password = models.CharField(
#         max_length=128,
#         validators=[validate_password]
#     )

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        unique=True,
        validators=[validate_email]
    )
    password = models.CharField(
        max_length=128,
        validators=[validate_password]
    )

    @property
    def has_active_subscription(self):
        # TODO: Replace with real logic if using Stripe or another subscription system
        return True  # Temporary dummy implementation
    

def user_directory_path(instance, filename):
    """File upload path for documents."""
    return f'user_{instance.user.id}/{filename}'

class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=user_directory_path)  # Use relative path
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=10, default='pdf')

    class Meta:
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = os.path.basename(self.file.name)
        if not self.file_type:
            ext = os.path.splitext(self.file.name)[1][1:].lower()
            self.file_type = ext if ext else 'pdf'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.file_type})"

class AnalysisResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    extracted_text = models.TextField()
    analysis_data = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Analysis of {self.document.title}"

class UploadedPDF(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255, blank=True)
    pdf_file = models.FileField(upload_to=user_directory_path)  # Use relative path
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_analyzed = models.BooleanField(default=False)
    chunk_metadata = JSONField(default=list, blank=True)
    faiss_index = models.BinaryField(null=True, blank=True)

    class Meta:
        verbose_name = "Uploaded PDF"
        verbose_name_plural = "Uploaded PDFs"
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        if not self.file_name:
            self.file_name = os.path.basename(self.pdf_file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name
    

# def cancel(self):
#     self.status = 'cancelled'
#     self.save()
