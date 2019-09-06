from django import forms

from .models import Drive

'''
class DateInput(forms.DateInput):
    input_type = 'date'

class DriveDataForm(forms.Form):
    date = forms.DateField(widget=DateInput)

'''
class DriveDataForm(forms.ModelForm):
    class Meta():
        model = Drive
        fields = ('company_name', 'date', 'venue', 'time', 'rounds', 'login_key', 'eligibility', 'base_package', 'campus_type', 'drive_id',)
