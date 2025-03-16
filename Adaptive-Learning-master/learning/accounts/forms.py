from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

# for not a valid email-address.
class EmailValidationOnForgotPassword(PasswordResetForm):

	def clean_email(self):
		
		email = self.cleaned_data['email']
		if not User.objects.filter(email__iexact=email,is_active=True).exists():
			msg = ('There is no User registered with the specified E-mail address.')
			self.add_error('email',msg)
		return email
	

from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Enter password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Confirm password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['user']  # We handle the user manually in the view
