from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserChangeForm

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Enter password', 
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = [ 'first_name', 'last_name','email','password1', 'password2']

class CustomUserUpdateForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = [  'first_name','last_name', 'email', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    
    #Init function to remove password field from update form
    def __init__(self, *args, **kwargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields.pop('password', None)