from django.urls import path
from . import views

urlpatterns = [
    path('time_checkbox', views.create_time.as_view(), name="time_checkbox")
]
