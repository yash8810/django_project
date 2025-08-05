from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    first_name = models.CharField(max_length=100, db_column='FitFusion.ai_user_first_name')  # First Name
    last_name = models.CharField(max_length=100, db_column='FitFusion.ai_user_last_name')  # Last Name
    email = models.EmailField(unique=True, db_column='FitFusion.ai_user_email')  # Email Address
    contact_number = models.CharField(max_length=15, blank=True, null=True, db_column='FitFusion.ai_user_contact_number')  # Contact Number
    password = models.CharField(max_length=255, db_column='FitFusion.ai_user_password')  # Store hashed password
    newsletter_signup = models.BooleanField(default=False, db_column='FitFusion.ai_newsletter_signup')  # Newsletter signup checkbox
    last_login = models.DateTimeField(null=True, blank=True)  # Required for auth_login
    is_active = models.BooleanField(default=True)  # Required for authentication
    is_staff = models.BooleanField(default=False)

    gender = models.CharField(
        max_length=10, 
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], 
        db_column='FitFusion.ai_user_gender',
        blank=True,  # Allow blank value for initial state
        null=True,  # Allow null value in database until updated
    )
    height = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        db_column='FitFusion.ai_user_height'
    )  # Height in cm
    weight = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        db_column='FitFusion.ai_user_weight'
    )  # Weight in kg
    dob = models.DateField(
        null=True, 
        blank=True, 
        db_column='FitFusion.ai_user_dob'
    )  # Date of birth
    age = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        db_column='FitFusion.ai_user_age'
    )  # Age
    goal = models.CharField(
        max_length=50, 
        choices=[('Weight Loss', 'Weight Loss'), ('Muscle Gain', 'Muscle Gain'), ('Maintain', 'Maintain')], 
        db_column='FitFusion.ai_user_goal',
        blank=True,  # Allow blank value for initial state
        null=True,  # Allow null value in database until updated
    )
    target_areas = models.CharField(
        max_length=255, 
        blank=True, 
        db_column='FitFusion.ai_user_target_areas'
    )  # Target areas (e.g. Abs, Legs)
    workout_experience = models.CharField(
        max_length=50, 
        choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], 
        db_column='FitFusion.ai_user_workout_experience',
        blank=True,  # Allow blank value for initial state
        null=True,  # Allow null value in database until updated
    )
    diet_preferences = models.CharField(
        max_length=50, 
        choices=[('Vegetarian', 'Vegetarian'), ('Vegan', 'Vegan'), ('Non-Vegetarian', 'Non-Vegetarian'), ('Pescatarian', 'Pescatarian')], 
        db_column='FitFusion.ai_user_diet_preferences',
        blank=True,  # Allow blank value for initial state
        null=True,  # Allow null value in database until updated
    )
    medical_conditions = models.CharField(
        max_length=255, 
        blank=True, 
        db_column='FitFusion.ai_user_medical_conditions',
        null=True,  # Allow null value in database until updated
    )  # Multiple medical conditions
    profile_image = models.ImageField(
        upload_to='profile_images/', 
        null=True, 
        blank=True, 
        db_column='FitFusion.ai_user_profile_image'
    )  # Profile image
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
   
  #  def save(self, *args, **kwargs):
   #     if self.password and not self.password.startswith('pbkdf2_sha256$'):
    #        self.password = make_password(self.password)  # Hash only if not already hashed
     #       super().save(*args, **kwargs)


   
    class Meta:
        db_table = 'FitFusionai_user'
