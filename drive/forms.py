from django import forms
from django.contrib.auth.models import User
from .models import Drive


class DriveData(forms.ModelForm):
    class Meta():
        model = Drive
        fields = ('company_name', 'date', 'venue', 'time', 'rounds', 'login_key', 'eligibility', 'base_package', 'campus_type', 'drive_id',)
