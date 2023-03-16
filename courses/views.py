from django.shortcuts import render, redirect
from .models import TeacherTime
from datetime import date, timedelta, datetime


def create_time(request):

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    if request.method == "POST":
        date_list = []
        teacher_time_list = request.POST.getlist('times')

        start_date = date.today()
        end_date = date(2024, 1, 1)

        for single_date in daterange(start_date, end_date):
            d = single_date.strftime("%Y-%m-%d")
            for t in teacher_time_list:
                if single_date.weekday() == int(t[0]):
                    t_time = TeacherTime.objects.create(date=d, start=t[2:])
                    t_time.save()

        return redirect('account_details')
    return render(request, 'courses/time_checkbox.html')



