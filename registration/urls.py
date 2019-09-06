from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView, name = 'login'),
    url('signup/', views.register, name ='signup'),
    path('single_student/', views.single_student, name='single_student'),
]
