from django.shortcuts import render, redirect
from . import models
from datetime import date, timedelta, datetime


def create_time(request):

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    if request.method == "POST":
        date_list = []
        start_date = date.today()
        end_date = date(2024, 1, 1)
        for single_date in daterange(start_date, end_date):
            date_list.append(single_date.strftime("%Y-%m-%d"))
            print(date_list)

        time = request.POST.getlist('times')
        print(time)

        return redirect('account_details')
    return render(request, 'courses/time_checkbox.html')



