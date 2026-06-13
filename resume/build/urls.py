from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('resume/', views.resume_page, name='resume_page'),
    path('resume-list/', views.list_resumes, name='list_resumes'),
    path('resume/<int:id>/', views.resume_detail, name='resume_detail'),
    path('send-request/', views.send_request, name='send_request'),
    path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('resume/detail/<int:id>/', views.resume_detail, name='resume_detail'),
    path('accept-request/<int:id>/', views.accept_request, name='accept_request'),
    path('research-request/', views.research_request, name='research_request'),
    path('teacher-profile/<str:username>/', views.teacher_profile, name='teacher_profile'),
    path('update-teacher-info/', views.update_teacher_info, name='update_teacher_info'),
    path('logout/', views.logout_user, name='logout'),
    
]