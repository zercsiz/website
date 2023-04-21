from django.urls import path
from . import views

urlpatterns = [
    path('time_checkbox', views.CreateTime.as_view(), name="time_checkbox"),
    path('teacher_details/<int:teacher_id>/<str:teacher_slug>/', views.TeacherDetails.as_view(), name="teacher_details"),
    path('delete_teacher_plan/<int:plan_id>', views.DeleteTeacherPlanView.as_view(), name="delete_teacher_plan"),
    path('teacher_time_report/<int:teacher_time_id>', views.TeacherTimeReportView.as_view(), name="teacher_time_report"),
    path('google_meet_link_tutorial/', views.GoogleMeetLinkTutorialView.as_view(), name="google_meet_link_tutorial")
]
