from django.urls import path
from . import views

urlpatterns = [
    path('time_checkbox', views.CreateTime.as_view(), name="time_checkbox")
]
