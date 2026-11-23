from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("resume/upload/", views.upload_resume, name="upload_resume"),
    path("interview/", views.start_interview, name="start_interview"),
    path("interview/upload/", views.upload_video, name="upload_video"),
    path("staff/login/", views.admin_login, name="admin_login"),
    path("staff/logout/", views.admin_logout, name="admin_logout"),
    path("staff/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("staff/candidates/<int:candidate_id>/status/", views.update_status, name="update_status"),
    path("staff/interviews/<int:id>/score/", views.score_interview, name="score_interview"),
    path("staff/interviews/<int:id>/accept/", views.accept_interview, name="accept_interview"),
    path("staff/interviews/<int:id>/reject/", views.reject_interview, name="reject_interview"),
]
