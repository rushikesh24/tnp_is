from django.conf.urls import url

from . import views

urlpatterns = [
    url('driveupload/', views.drive_upload, name='drive'),
    url('round_details/', views.drive_upload, name='round_details'),
    url('student_attendance/', views.student_attendence, name='student_attendance'),
]