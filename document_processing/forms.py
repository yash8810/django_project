from django import forms
from .models import UploadedPDF  # Import the model where PDFs should be stored

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedPDF
        fields = ["file_name", "pdf_file"]


class QueryForm(forms.Form):
    query = forms.CharField(label="Enter your question", max_length=1000)