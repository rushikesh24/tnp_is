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
    id = models.CharField(max_length=10, null=False, blank=False, primary_key=True)
    name = models.CharField(max_length=80, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    birthdate = models.DateField(auto_now=False, auto_now_add=False)
    tenth = models.DecimalField(max_digits=5, decimal_places=2)
    diploma_12 = models.DecimalField(max_digits=5, decimal_places=2)
    branch = models.CharField(max_length=50, null=False, blank=False)
    gender = models.CharField(max_length=2, null=False,default='Male', blank=False)
    placed = models.BooleanField(default=False)
    primary_mobile = models.CharField(max_length=10, null=False, blank=False)
    secondary_mobile = models.CharField(max_length=10, blank=True)
    attendence_status = models.BooleanField(default=False)
    marks = models.ArrayModelField(model_container=Year_marks)
    avg_marks = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=False, blank=False)
    designation = models.CharField(max_length=50, null=False, blank=False)
    department = models.CharField(max_length=50, null=False, blank=False)
    primary_mobile = models.CharField(max_length=10, null=False, blank=False)
    gender = models.CharField(max_length=10,default='Male', null=False, blank=False)
    secondary_mobile = models.CharField(max_length=10, blank=True)
    email = models.EmailField(max_length=50,null=False,blank=False)

    def __str__(self):
        return self.user.username
