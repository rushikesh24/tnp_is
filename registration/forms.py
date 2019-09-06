from django import forms
from django.contrib.auth.models import User

from .models import Employee
from .models import Student


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = Employee
        fields = ('name', 'designation', 'department', 'primary_mobile', 'secondary_mobile', 'email')


class StudentDataForm(forms.ModelForm):
    class Meta():
        model= Student
        fields = ('_id', 'name', 'email', 'tenth', 'diploma_12', 'branch', 'gender', 'placed', 'primary_mobile',
                  'secondary_mobile', 'marks',)  # , 'birthdate')
