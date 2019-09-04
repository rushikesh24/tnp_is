from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    url('drive_upload/', views.drive_upload, name='drive')
]