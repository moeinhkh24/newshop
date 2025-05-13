from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model#مدل سفارشی یوزر
from django.contrib.auth.forms import ReadOnlyPasswordHashField
import re
from .validators import valid_phone_number
#CreateForm , ChangeForm

class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)#lable برای ظاهر سایت برای پسورد و تایید پسورد

    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'email', 'username', 'fullname']

    def clean_password(self):
        cd = self.cleaned_data #داده های اعتبار سنجی شده

        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('Password must match')

        return cd['password2']

    def save(self, commit: bool):
        cd = self.cleaned_data
        user = super().save(commit=False)#super یعنی برگرد کلاس مادر
        user.set_password(cd['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password =ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\"this form</a>.")

    class Meta:
        model = get_user_model()
        fields = '__all__'


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=11,validators=[valid_phone_number])
    email = forms.EmailField()
    username = forms.CharField(max_length=55)
    fullname = forms.CharField(max_length=125)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not re.match(r'^09\d{9}$',phone_number):
            raise ValidationError("Phone Number must be phone Number")
        user = get_user_model().objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError("This Phone number is already exists")
        OtpCode.objects.filter(phone = phone_number).delete()
        return phone_number
    def clean_email(self):
        email = self.cleaned_data['email']
        #TODO ----> Create Regex for email

        user = get_user_model().objects.filter(email=email).exists()
        if user:
            raise ValidationError("This email is already exists")
        return email

class OtpForm(forms.Form):
    code = forms.IntegerField()

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(max_length=11,widget=forms.PasswordInput)
