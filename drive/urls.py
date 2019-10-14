from django.conf.urls import url

from . import views

urlpatterns = [
    url('upload/', views.drive_upload, name='drive_upload'),
    url('round/details/', views.drive_upload, name='round_details'),
    url('student/attendance/', views.student_attendence, name='student_attendance'),
    url('student/list/', views.student_list, name='student_list'),
    url('volunteer/search', views.volunteer_search, name='volunteer_search'),
    url('volunteer/update/', views.volunteer_update, name='volunteer_update'),
    url('company/search', views.company_search, name="company_search"),
    url('placed/details', views.placed_details, name="placed_details"),
    url('placed/analysis', views.placed_analysis, name='placed_analysis'),
    url('college/analysis', views.college_analysis, name='college_analysis'),
    url('total/analysis', views.total_analysis, name='total_analysis'),
    url('company/analysis', views.company_analysis, name='company_analysis'),
    url('report/pdf',views.report_pdf,name='report_pdf'),
]