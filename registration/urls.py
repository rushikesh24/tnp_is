from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('login/', auth_views.LoginView, name='employee_login'),
    url('employee/signup/', views.employee_registeration, name='employee_signup'),
    url('student/details/', views.candidate_upload, name='student_details'),
]
