from djongo import models

class Drive_Rounds(models.Model):
    round1 = models.CharField(max_length=20, default='Aptitude Round', blank=False)
    round2 = models.CharField(max_length=20, default='Technical Round', blank=False)
    round3 = models.CharField(max_length=20, default='Interview Round', blank=False)
    round4 = models.CharField(max_length=20, default='HR Round', blank=False)
    round5 = models.CharField(max_length=20)

class Eligibility(models.Model):
    tenth_marks = models.DecimalField(max_digits=5, decimal_places=3)
    diploma_12 = models.DecimalField(max_digits=5, decimal_places=3)
    engg = models.DecimalField(max_digits=5, decimal_places=3)


class Attendence(models.Model):
    _id = models.CharField(max_length=10, null=False, blank=False, primary_key=True, unique=True)
    name = models.CharField(max_length=80, null=False, blank=False)
    branch = models.CharField(max_length=50, null=False, blank=False)

class Drive(models.Model):
    _id = models.CharField(max_length=10, null=False, blank=False, primary_key=True, unique=True)
    company_name = models.CharField(max_length=20, null=False, blank=False)
    date = models.CharField(max_length=10, null=False, blank=False)
    venue = models.CharField(max_length=10, blank=False, null=False)
    branch = models.CharField(max_length=100, blank=False, null=False)
    time = models.CharField(max_length=15, null=False, blank=False)
    rounds = models.EmbeddedModelField(model_container=Drive_Rounds)
    login_key = models.CharField(max_length=15, null=False, blank=False)
    eligibility = models.EmbeddedModelField(model_container=Eligibility)
    base_package = models.DecimalField(max_digits=8, decimal_places=3, default='00', blank=False, null=False)
    campus_type = models.CharField(max_length=10, null=False, blank=False)
    eligible_student = models.EmbeddedModelField(model_container=Attendence)
    round1_student = models.EmbeddedModelField(model_container=Attendence)
    round2_student = models.EmbeddedModelField(model_container=Attendence)
    round3_student = models.EmbeddedModelField(model_container=Attendence)
    round4_student = models.EmbeddedModelField(model_container=Attendence)
    round5_student = models.EmbeddedModelField(model_container=Attendence)
    round6_student = models.EmbeddedModelField(model_container=Attendence)
    round7_student = models.EmbeddedModelField(model_container=Attendence)
    round8_student = models.EmbeddedModelField(model_container=Attendence)
