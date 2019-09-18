from djongo import models


class Drive_Rounds(models.Model):
    round_name = models.CharField(max_length=20, blank=False)
    round_number = models.CharField(max_length=2, blank=False)

    class Meta:
        abstract = True


class Eligibility(models.Model):
    tenth_marks = models.DecimalField(max_digits=5, decimal_places=3)
    diploma_12 = models.DecimalField(max_digits=5, decimal_places=3)
    engineering = models.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        abstract = True


class Attendance(models.Model):
    _id = models.CharField(max_length=10, null=False, blank=False, primary_key=True, unique=True)
    name = models.CharField(max_length=80, null=False, blank=False)
    branch = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        abstract = True


class Drive(models.Model):
    _id = models.CharField(max_length=60, null=False, blank=False, primary_key=True, unique=True)
    company_name = models.CharField(max_length=50, null=False, blank=False)
    date = models.CharField(max_length=10, null=False, blank=False)
    time = models.CharField(max_length=15, null=False, blank=False)
    venue = models.CharField(max_length=100, blank=False, null=False)
    campus_type = models.CharField(max_length=10, null=False, blank=False)
    branch = models.CharField(max_length=100, blank=False, null=False)
    base_package = models.DecimalField(max_digits=8, decimal_places=3, blank=False, null=False)
    login_key = models.CharField(max_length=15, null=False, blank=False)
    rounds = models.ArrayModelField(model_container=Drive_Rounds)
    eligibility = models.ArrayModelField(model_container=Eligibility)
    eligible_student = models.ArrayModelField(model_container=Attendance)
    round1_student = models.ArrayModelField(model_container=Attendance)
    round2_student = models.ArrayModelField(model_container=Attendance)
    round3_student = models.ArrayModelField(model_container=Attendance)
    round4_student = models.ArrayModelField(model_container=Attendance)
    round5_student = models.ArrayModelField(model_container=Attendance)
    round6_student = models.ArrayModelField(model_container=Attendance)
    round7_student = models.ArrayModelField(model_container=Attendance)
    round8_student = models.ArrayModelField(model_container=Attendance)
    placed_student = models.ArrayModelField(model_container=Attendance)
