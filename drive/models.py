from djongo import models


class Drive_Rounds(models.Model):
    round_1 = models.CharField(max_length=20, default='Aptitude Round', blank=False)
    round_2 = models.CharField(max_length=20, default='Technical Round', blank=False)
    round_3 = models.CharField(max_length=20, default='Interview Round', blank=False)
    round_4 = models.CharField(max_length=20, default='HR Round', blank=False)
    round_5 = models.CharField(max_length=20)

class Eligibility(models.Model):
    tenth_marks = models.DecimalField(max_digits=5, decimal_places=3)
    diploma_12 = models.DecimalField(max_digits=5, decimal_places=3)
    engg = models.DecimalField(max_digits=5, decimal_places=3)

class Drive(models.Model):
    _id = models.CharField(max_length=10, null=False, blank=False, primary_key=True, unique=True)
    company_name = models.CharField(max_length=20, null=False, blank=False)
    # date = models.DateField(auto_now=False, auto_now_add=False)
    venue = models.CharField(max_length=10, blank=False, null=False)
    branch = models.CharField(max_length=100, blank=False, null=False)
    # time = models.TimeField(auto_now_add=False, auto_now=False)
    rounds = models.EmbeddedModelField(model_container=Drive_Rounds)
    login_key = models.CharField(max_length=15, null=False, blank=False)
    eligibility = models.EmbeddedModelField(model_container=Eligibility)

    base_package = models.DecimalField(max_digits=8, decimal_places=3, default='00', blank=False, null=False)
    campus_type = models.CharField(max_length=10, null=False, blank=False)
