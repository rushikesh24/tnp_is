from django.contrib.auth.models import User
from djongo import models
import datetime
from django.db.models.fields import DateField
from django.utils.dateparse import parse_datetime


class Drive_Rounds(models.Model):
    round_1 = models.CharField(max_length=10, default='MCQ_Round',blank=False)
    round_2 = models.CharField(max_length=10, default='Technical_Round',blank=False)
    round_3 = models.CharField(max_length=10, default='Interview_Round',blank=False)
    round_4 = models.CharField(max_length=10, default='HR_Round',blank=False)
    round_5 = models.CharField(max_length=10)

class Eligibility(models.Model):
    tenth_marks = models.DecimalField(max_digits=5, decimal_places=3)
    diploma_12 = models.DecimalField(max_digits=5, decimal_places=3)
    engg = models.DecimalField(max_digits=5, decimal_places=3)

class Drive(models.Model):
    drive_id = models.CharField(max_length=10, null=False, default='000',blank=False, primary_key=True, unique=True)
    company_name = models.CharField(max_length=20, null=False, blank=False)
    date = models.DateField(auto_now=False, auto_now_add=False)
    venue = models.CharField(max_length=10, blank=False, default='DYPCOE_TNP', null=False)
    time = models.TimeField(auto_now_add=False, auto_now=False)
    rounds = models.ArrayModelField(model_container=Drive_Rounds)
    login_key = models.CharField(max_length=15, null=False, blank=False)
    eligibility = models.ArrayModelField(model_container=Eligibility)
    base_package = models.CharField(max_length=10, default='00', blank=False, null=False)
    campus_type = models.CharField(max_length=10, null=False, blank=False)

