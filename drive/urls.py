from django.conf.urls import url

from . import views

urlpatterns = [
    url('upload/', views.drive_upload, name='drive_upload'),
    url('round/details/', views.drive_upload, name='round_details'),
    url('student/attendance/', views.student_attendence, name='student_attendance'),
    url('student/list/', views.student_list, name='student_list'),
    url('report/generation/student/placed',views.report_generation_placed,name='report_generation_placed'),
    #url('report/round1',views.report_for_round1,name='report_round1'),
    url('volunteer/', views.volunteer, name='volunteer'),
    url('volunteer/update/', views.volunteer_update, name='volunteer_update'),
]