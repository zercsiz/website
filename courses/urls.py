from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CoursesView.as_view(), name="home"),
    path('search', views.CoursesSearchView.as_view(), name="search"),
    path('course_details/<int:course_id>', views.CourseDetailsView.as_view(), name="course_details"),
]
