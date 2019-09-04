from django import forms
from .models import Employee
from django.contrib.auth.models import User
from .models import Student

gender_choices = ['m', 'f', 'o']
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = Employee
        fields = ('name', 'designation', 'department', 'primary_mobile', 'secondary_mobile', 'email')

class StudentData(forms.ModelForm):
    class Meta():
        model= Student
        fields =('name','email', 'branch', 'primary_mobile', 'secondary_mobile','tenth','diploma_12','gender','marks','_id','placed', 'birthdate')