from django.contrib.auth.models import User
from djongo import models

# Create your models here.

'''Candidate Model'''

class Candidate(models.Model):
    clg_name = (('dypcoe', 'DYPCOE'), ('dypiemr', 'DYPIEMR'))
    branch_choice = (('computer', 'Computer Engineering'),
                     ('information technology', 'Information Engineering'),
                     ('entc', 'E&TC Engineering'),
                     ('production', 'Production Engineering'),
                     ('instrumentation', 'Instrumentation Engineering'),
                     ('civil', 'Civil Engineering'),
                     ('mechanical', 'Mechanical Engineering')
                    )


    # personal details
    _id = models.CharField(max_length=10, null=False, blank=False, primary_key=True, unique=True)
    name = models.CharField(max_length=80, null=False, blank=False)
    gender = models.CharField(max_length=10, default="Male", null=False, blank=False)
    aadhar_number = models.DecimalField(max_digits=12, decimal_places=0, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    primary_mobile = models.CharField(max_length=10, null=False, blank=False)
    secondary_mobile = models.CharField(max_length=10, blank=True)
    # educational details
    tenth = models.DecimalField(max_digits=5, decimal_places=2)
    diploma_12 = models.DecimalField(max_digits=5, decimal_places=2)
    college_name = models.CharField(max_length=20, choices=clg_name, default='DYPCOE', null=False, blank=False)
    branch = models.CharField(max_length=50, choices=branch_choice, default='Computer', null=False, blank=False)
    engineering = models.DecimalField(max_digits=5, decimal_places=2)
    live_backlog = models.BooleanField(default=False)
    # placement details
    placed = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    eligible = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    round1 = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    round2 = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    round3 = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    round4 = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    round5 = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    round6 = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    round7 = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    round8 = models.DecimalField(max_digits=3, decimal_places=0, default=0)

    def __str__(self):
        return self.name


'''Employee Model'''
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=False, blank=False)
    name = models.CharField(max_length=80, null=False, blank=False)
    gender = models.CharField(max_length=10, default="Male", null=False, blank=False)
    department = models.CharField(max_length=50, null=False, blank=False)
    designation = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    primary_mobile = models.CharField(max_length=10, null=False, blank=False)
    secondary_mobile = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.user.username
