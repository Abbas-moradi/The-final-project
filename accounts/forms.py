from django import forms
from .models import User, Address
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


"""
This form is used to create a new user.
It collects information such as email, phone number, full name, and password. 
It also includes fields for password confirmation. In this form,
the clean_password2 method is defined for password validation.
"""
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def cleanpassword2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


"""
This form is used to edit existing user information.
It allows the user to change email, phone number, full name, and password.
However, the password is displayed as a read-only field.
"""

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change password using <a href=\'../password/\'>this form</a>')

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')

"""
These two forms are used for user registration. 
They collect information such as full name, email, phone number, and password.
Additionally, in both forms, the clean_email and clean_phone methods are defined
 to check for duplicate email and phone number entries.
"""

class UserRegisterForm(forms.Form):
    full_name = forms.CharField(label='full name')
    email = forms.EmailField()
    phone = forms.CharField(max_length=13)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterationForm(forms.Form):
    full_name = forms.CharField(label='full name')
    email = forms.EmailField()
    phone = forms.CharField(max_length=13)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exists')
        return email
        
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('this phone number already exists')
        return phone
    
"""
 This form is used for user login and includes fields
   for entering the phone number and password.
"""

class UserLoginForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


"""
These two forms are used to verify a code sent to the user
for confirmation purposes (e.g., phone number verification).
They include an input field for entering the verification code.
"""

class VerifyCodeForm(forms.Form):
    code = forms.CharField()

class VerifyForm(forms.Form):
    code = forms.CharField()


"""
This form is used to create new addresses by users.
 It collects information such as province, city, street,
   and license plate number.
"""
class AddAddress(forms.Form):
    province = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    street = forms.CharField(max_length=100)
    license_plate = forms.IntegerField()


class AddressSelectionForm(forms.Form):
    address_id = forms.IntegerField(widget=forms.HiddenInput())
    main_address = forms.BooleanField(widget=forms.HiddenInput(), required=False)