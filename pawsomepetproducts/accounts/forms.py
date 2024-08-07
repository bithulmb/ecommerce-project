from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Address
from django import forms
from django.contrib.auth.forms import UserChangeForm
import re
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

#User Sign Up Form
class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Enter password', 
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = [ 'first_name', 'last_name','email','phone_number','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Customize error messages for built-in fields
        self.fields['email'].error_messages['required'] = 'Please enter your email address.'
        self.fields['email'].error_messages['unique'] = 'This email address is already registered.'   
    
    #phonenumber validator function    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not re.match(r'^\+?1?\d{10,12}$', phone_number):
            raise forms.ValidationError("Phone number can only contain digits and + sign. 10 to 12 digits allowed.")
        return phone_number
    
    #first name validator function
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[a-zA-Z\s]+$', first_name):
            raise forms.ValidationError('Name can only contain letters.')
        return first_name
    

    #last name validator function
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[a-zA-Z\s]+$', last_name):
            raise forms.ValidationError('Name can only contain letters.')
        return last_name

#user edit form for admin
class CustomUserUpdateForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = [  'first_name','last_name', 'email', 'phone_number', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    
    #Init function to remove password field from update form
    def __init__(self, *args, **kwargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields.pop('password', None)

#user edit form for user
class UserProfileForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields = [  'first_name','last_name', 'email', 'phone_number']
        widgets = {
           
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        }
    #phonenumber validator function    
    def clean_phone_number(self):
        phonenumber = self.cleaned_data.get('phone_number')
        if phonenumber and not re.match(r'^\+?1?\d{9,12}$', phonenumber):
            raise forms.ValidationError("Phone number can only contain digits and + sign. 9 to 12 digits allowed.")
        return phonenumber
    
    #first name validator function
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[a-zA-Z\s]+$', first_name):
            raise forms.ValidationError('Name can only contain letters.')
        return first_name
    

    #last name validator function
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[a-zA-Z\s]+$', last_name):
            raise forms.ValidationError('Name can only contain letters.')
        return last_name


#Add address form for user
class AddAddressForm(forms.ModelForm):
    class Meta:
        model=Address
        exclude=['user','is_default']

class OTPVerificationForm(forms.Form):
    otp=forms.CharField(label="Enter the OTP", max_length=10,min_length=6)

