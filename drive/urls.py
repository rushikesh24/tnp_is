from django.conf.urls import url

from . import views

urlpatterns = [
    url('upload/', views.drive_upload, name='drive_upload'),
    url('round/details/', views.drive_upload, name='round_details'),
    url('student/attendance/', views.student_attendence, name='student_attendance'),
    url('student/list/', views.student_list, name='student_list'),
    url('report/generation/student/placed',views.report_generation_placed, name='report_generation_placed'),
    url('volunteer/search', views.volunteer_search, name='volunteer_search'),
    url('volunteer/update/', views.volunteer_update, name='volunteer_update'),
    url('company/search',views.company_search,name="company_search"),
    url('placed/details',views.placed_details,name="placed_details"),
    url('report/round1',views.placed_analysis, name='report_round1'),
]