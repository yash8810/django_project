from django import forms
from django.contrib.auth.hashers import check_password
from .models import User

class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=255)  # To match password with confirmation

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'contact_number', 'password', 'newsletter_signup']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, label="Password", max_length=255)
    
    class Meta:
        model = User
        fields = ['email', 'password']
    
    def clean_email(self):
        """ Validate email and ensure the user exists """
        email = self.cleaned_data.get('email')
        
        try:
            # Check if the user exists in the database
            user = User.objects.get(email=email)
            self.user = user  # Store the user object for later use
        except User.DoesNotExist:
            raise forms.ValidationError("User with this email does not exist.")
        
        return email
    
    def clean_password(self):
        """ Validate the password by checking it against the stored hash """
        password = self.cleaned_data.get('password')
        
        # Compare the password with the hash stored in the database
        if self.user and not check_password(password, self.user.password):
            raise forms.ValidationError("Incorrect password.")
        
        return password

