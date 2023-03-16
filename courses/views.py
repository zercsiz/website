from django.shortcuts import render
from . import models


def create_time(request):
    if request.method == "POST":
        time = request.POST.getlist('times')
        print(time)
    return render(request, 'courses/time_checkbox.html')
