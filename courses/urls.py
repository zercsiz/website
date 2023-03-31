from django.urls import path
from . import views

urlpatterns = [
    path('time_checkbox', views.CreateTime.as_view(), name="time_checkbox"),
    path('teacher_details/<int:teacher_id>/', views.TeacherDetails.as_view(), name="teacher_details")
]
