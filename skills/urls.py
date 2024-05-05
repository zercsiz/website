from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.SkillsView.as_view(), name='skills_home'),
    path('skill_details/<int:skill_id>/<str:skill_slug>/', views.SkillDetailsView.as_view(), name="skill_details"),
]