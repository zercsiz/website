from django.shortcuts import render, redirect
from .models import *
from shop.models import *
from datetime import date, timedelta, datetime
from accounts.models import Account
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from jalali_date import date2jalali


class CreateTime(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin
    def post(self, request):

        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

        # this function converts weekday number to farsi weekday names
        def week_day_convert(day_number):
            # here shanbe is 5
            day_list = ['دوشنبه','سه شنبه','چهارشنبه','پنجشنبه','جمعه','شنبه','یکشنبه',]
            return day_list[day_number]

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
            price = int(request.POST.get('price'))
            teacher = request.user

            start_date = date.today()
            end_date = date(2023, 12, 1)

            # TeacherPlan creation
            t_plan, created = TeacherPlan.objects.get_or_create(teacher=teacher)

            for single_date in daterange(start_date, end_date):
                d = date2jalali(single_date).strftime("%Y-%m-%d")

                for t in teacher_time_list:
                    end_time = str(calculate_endtime(t[2:]))
                    if single_date.weekday() == int(t[0]):

                        # PlanTime creation
                        p_time, created = PlanTime.objects.get_or_create(teacherplan=t_plan, week_day=week_day_convert(int(t[0])),
                                          start=t[2:], end=end_time)

                        # TeacherTime creation
                        t_time, created = TeacherTime.objects.get_or_create(date=d, gdate=single_date.strftime("%Y-%m-%d"),
                                                                   week_day=week_day_convert(int(t[0])), start=t[2:],
                                                                   end=end_time, price=price,
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


class TeacherDetails(View):
    def get(self, request, teacher_id):
        teacher_time = TeacherTime.objects.filter(teacher=teacher_id).filter(gdate__gt=date.today())
        teacher = Account.objects.get(id=teacher_id)
        w_days = ("شنبه", "یکشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنجشنبه", "جمعه",)
        try:
            t_plan = TeacherPlan.objects.get(teacher=teacher)
        except TeacherPlan.DoesNotExist:
            t_plan = None
        if t_plan:
            p_time = PlanTime.objects.filter(teacherplan=t_plan)
            teacher_time_list = TeacherTime.objects.all()
            context = {
                'teacher': teacher,
                'teacher_time': teacher_time,
                'plan_times': p_time,
                'week_days': w_days
            }
        else:
            context = {
                'teacher': teacher,
                'teacher_time': teacher_time,
                'week_days': w_days
            }
        return render(request, 'courses/teacher_details.html', context)

    def post(self, request, teacher_id):
        order, created = Order.objects.get_or_create(student=request.user)
        p_times_ids = request.POST.getlist('p_time_id')
        p_times = []
        for id in p_times_ids:
            p_times.append(PlanTime.objects.get(id=id))

        # this gets the teacher id from the first plan time
        teacher = p_times[0].teacherplan.teacher

        start_date = date.today()
        teacher_times = TeacherTime.objects.filter(teacher=teacher).filter(gdate__gt=start_date).filter(is_reserved=False)
        session_number = request.POST.get('session_number')
        order_items = []

        # these fors create orderItems based on days and start times
        for t_time in teacher_times:
            for p in p_times:
                if p.week_day == t_time.week_day and p.start == t_time.start:
                    order_item, created = OrderItem.objects.get_or_create(teacherTime=t_time, order=order)
                    order_items.append(order_item)
                    break
            if len(order_items) == int(session_number):
                break

        context = {'order_items': order_items,
                   'items': []}
        return render(request, 'shop/cart.html', context)
