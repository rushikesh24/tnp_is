from djongo import models

# Create your models here.

class Year_marks(models.Model):
    FE = models.DecimalField(max_digits=4, decimal_places=2,null=False,blank=False,default=0.00)
    SE = models.DecimalField(max_digits=4, decimal_places=2,null=False,blank=False,default=0.00)
    TE = models.DecimalField(max_digits=4, decimal_places=2,null=False,blank=False,default=0.00)
    BE = models.DecimalField(max_digits=4, decimal_places=2,null=False,blank=False,default=0.00)
    class Meta:
        abstract = True

class Student(models.Model):
    pnr = models.CharField(max_length=10, null=False, blank=False, primary_key=True)
    name = models.CharField(max_length=80,null=False,blank=False)
    email = models.EmailField(max_length=50,null=False,blank=False)
    birthdate = models.DateField(auto_now=False, auto_now_add=False)
    tenth = models.DecimalField(max_digits=5, decimal_places=2)
    diploma_12 = models.DecimalField(max_digits=5, decimal_places=2)
    branch = models.CharField(max_length=50,null=False,blank=False)
    gender = models.CharField(max_length=2,null=False,blank=False)
    placed = models.BooleanField(default=False)
    primary_mobile = models.CharField(max_length=10,null=False,blank=False)
    secondary_mobile = models.CharField(max_length=10,blank=True)
    attendence_status = models.BooleanField(default=False)
    marks = models.ArrayModelField(model_container=Year_marks)
    avg_marks = models.DecimalField(max_digits=5, decimal_places=2)

class Employee(models.Model):
    id = models.CharField(max_length=10, null=False, blank=False,primary_key=True)
    name = models.CharField(max_length=80, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    birthdate = models.DateField(auto_now=False, auto_now_add=False)
    designation = models.CharField(max_length=50, null=False, blank=False)
    gender = models.CharField(max_length=2, null=False, blank=False)
    department = models.CharField(max_length=50,null=False,blank=False)
    approved = models.BooleanField(default=False)
    primary_mobile = models.CharField(max_length=10, null=False, blank=False)
    secondary_mobile = models.CharField(max_length=10,blank=True)
    password = models.CharField(max_length=16,null=False,blank=False)