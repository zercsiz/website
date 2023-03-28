from django.shortcuts import render, redirect
from .models import TeacherTime
from datetime import date, timedelta, datetime
from accounts.models import Account
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateTime(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin
    def post(self, request):

        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

        # this function adds 1:30 to start time
        def calculate_endtime(start):
            start = start
            hour = int(start[0:2])
            minute = int(start[3:])
            end = timedelta(hours=hour, minutes=minute) + timedelta(hours=1, minutes=30)
            return end

        if request.user.is_teacher:
            teacher_time_list = request.POST.getlist('times')
            google_meet_link = request.POST.getlist('google_meet_link')

            start_date = date.today()
            end_date = date(2023, 12, 1)

            for single_date in daterange(start_date, end_date):
                d = single_date.strftime("%Y-%m-%d")
                for t in teacher_time_list:
                    end_time = str(calculate_endtime(t[2:]))
                    if single_date.weekday() == int(t[0]):
                        teacher = Account.objects.filter(phone_number=request.user.phone_number).first()
                        t_time = TeacherTime.objects.create(date=d, start=t[2:], end=end_time,
                                                            google_meet_link=google_meet_link[0], teacher=teacher)
                        t_time.save()

            return redirect('account_details')
        else:
            return redirect('home')

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_teacher:
                return render(request, 'courses/time_checkbox.html')
            else:
                return redirect('home')

        else:
            return redirect('user_login')

