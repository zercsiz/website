from django.shortcuts import render
from .models import Course
from accounts.models import Account


def home_view(request):
    teacher_list = Account.objects.get(is_teacher=True)[:6]
    course_list = Course.objects.all()[:6]
    context = {'courses': course_list, 'teachers': teacher_list}
    return render(request, 'home/home.html', context)

