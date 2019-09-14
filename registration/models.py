from django.contrib.auth.models import User
from djongo import models


# Create your models here.

class Year_marks(models.Model):
    FE = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False, default=0.00)
    SE = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False, default=0.00)
    TE = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False, default=0.00)
    BE = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False, default=0.00)

    class Meta:
        abstract = True


class Student(models.Model):
    _id = models.CharField(max_length=10, null=False, blank=False, primary_key=True, unique=True)
    name = models.CharField(max_length=80, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    # birthdate = models.DateField(auto_now=True, auto_now_add=False, null=True)
    tenth = models.DecimalField(max_digits=5, decimal_places=2)
    diploma_12 = models.DecimalField(max_digits=5, decimal_places=2)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    branch = models.CharField(max_length=50, null=False, blank=False)
    gender = models.CharField(max_length=10, null=False, default='Male', blank=False)
    placed = models.BooleanField(default=False)
    primary_mobile = models.CharField(max_length=10, null=False, blank=False)
    secondary_mobile = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=False, blank=False)
    designation = models.CharField(max_length=50, null=False, blank=False)
    department = models.CharField(max_length=50, null=False, blank=False)
    primary_mobile = models.CharField(max_length=10, null=False, blank=False)
    gender = models.CharField(max_length=10, null=False, default='Male', blank=False)
    secondary_mobile = models.CharField(max_length=10, blank=True)
    email = models.EmailField(max_length=50,null=False,blank=False)

    def __str__(self):
        return self.user.username
