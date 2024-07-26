from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Enter password', 
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = [ 'first_name', 'last_name','email', 'phone_number', 'password1', 'password2']