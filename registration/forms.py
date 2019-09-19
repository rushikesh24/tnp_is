from django import forms
from django.contrib.auth.models import User

from .models import Employee


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = Employee
        fields = ('name', 'designation', 'department', 'primary_mobile', 'secondary_mobile', 'email')
