from django.shortcuts import render
from .models import Course


def home_view(request):
    course_list = Course.objects.all()[:6]
    return render(request, 'home/home.html', {'courses': course_list})

