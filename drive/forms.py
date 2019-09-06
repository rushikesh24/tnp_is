from django import forms

from .models import Drive


class DriveDataForm(forms.ModelForm):
    class Meta():
        model = Drive
        fields = ('company_name', 'date', 'venue', 'time', 'rounds', 'login_key', 'eligibility', 'base_package', 'campus_type', 'drive_id',)
