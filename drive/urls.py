from django.conf.urls import url

from . import views

urlpatterns = [
    url('drive_upload/', views.drive_upload, name='drive')
]