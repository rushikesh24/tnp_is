from django.conf.urls import url

from . import views

urlpatterns = [
    url('driveupload/', views.drive_upload, name='drive')
]