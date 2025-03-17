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
from .models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'full_name', 'username', 'email', 'password', 'contact_no', 'gender', 
            'age_range', 'date_of_birth', 'address', 'disability', 'bio', 'account_type'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)