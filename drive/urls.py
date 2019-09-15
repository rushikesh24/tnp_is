from django.conf.urls import url

from . import views

urlpatterns = [
    url('upload/', views.drive_upload, name='drive_upload'),
    url('round_details/', views.drive_upload, name='round_details'),
    url('student_attendance/', views.student_attendence, name='student_attendance'),
    url('student_list/', views.student_list, name='student_list'),
]