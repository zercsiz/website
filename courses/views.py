from django.shortcuts import render, redirect
from .models import *
from shop.models import *
from datetime import date, timedelta, datetime
from accounts.models import Account
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from jalali_date import date2jalali


class CreateTime(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def post(self, request):

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
            google_meet_link = request.POST.get('google_meet_link')
            price = int(request.POST.get('price'))
            teacher = request.user

            # TeacherPlan creation
            t_plan, created = TeacherPlan.objects.get_or_create(teacher=teacher, google_meet_link=google_meet_link, price=price)

            # plantime creation
            for t in teacher_time_list:
                end_time = str(calculate_endtime(t[2:]))
                p_time, created = PlanTime.objects.get_or_create(teacherplan=t_plan, week_day=week_day_convert(int(t[0])),
                                start=t[2:], end=end_time, week_day_number=int(t[0]))

            return redirect('account_details')
        else:
            return redirect('home')

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_teacher:
                try:
                    plan = TeacherPlan.objects.get(teacher=request.user)
                except TeacherPlan.DoesNotExist:
                    plan = None
                if plan:
                    context = {'plan': plan}
                else:
                    context = {'plan': None}

                return render(request, 'courses/time_checkbox.html', context)
            else:
                return redirect('home')

        else:
            return redirect('user_login')


class TeacherDetails(View):
    def get(self, request, teacher_id):
        teacher = Account.objects.get(id=teacher_id)
        w_days = ("شنبه", "یکشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنجشنبه", "جمعه",)
        hours = ("09:00", "10:30", "12:00", "13:30", "15:00", "16:30", "18:00", "19:30")
        try:
            t_plan = TeacherPlan.objects.get(teacher=teacher)
        except TeacherPlan.DoesNotExist:
            t_plan = None
        if t_plan:
            p_times = PlanTime.objects.filter(teacherplan=t_plan)
            context = {
                'teacher': teacher,
                'plan_times': p_times,
                'week_days': w_days,
                'hours': hours
            }
        else:
            context = {
                'teacher': teacher,
            }
        return render(request, 'courses/teacher_details.html', context)

    def post(self, request, teacher_id):
        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

        if request.user.id == teacher_id:
            messages.error(request, "رزرو کردن تایم های خود امکان پذیر نیست", 'danger')
            return redirect('teacher_details', teacher_id)
        else:
            # create order for student
            order = Order.objects.create(student=request.user)
            order.save()

            p_times_ids = request.POST.getlist('p_time_id')

            p_times = []
            for i in p_times_ids:
                p_times.append(PlanTime.objects.get(id=i))

            # this gets the teacher id from the first plan time
            teacher = Account.objects.get(id=teacher_id)

            plan = TeacherPlan.objects.get(teacher=teacher)
            session_number = request.POST.get('session_number')
            order_items = []

            # start date and end date
            start_date = date.today()
            end_date = date(2023, 12, 1)

            for single_date in daterange(start_date, end_date):
                d = date2jalali(single_date).strftime("%Y-%m-%d")
                for p in p_times:
                    if single_date.weekday() == p.week_day_number:

                        # this checks whether the date and time is reserved and if it is, skips the day
                        try:
                            teacher_time = TeacherTime.objects.get(teacher=teacher, gdate=single_date.strftime("%Y-%m-%d"), start=p.start, is_reserved=True)
                        except TeacherTime.DoesNotExist:
                            teacher_time = None
                            print('none found')
                        if teacher_time:
                            break
                        else:
                            t_time, created = TeacherTime.objects.get_or_create(date=d, gdate=single_date.strftime("%Y-%m-%d"),
                                     week_day=p.week_day, start=p.start, end=p.end, price=plan.price,
                                     google_meet_link=plan.google_meet_link, teacher=teacher)
                            item = OrderItem.objects.get_or_create(teacherTime=t_time, order=order)
                            order_items.append(item)
                    if len(order_items) == int(session_number):
                        break
                if len(order_items) == int(session_number):
                    break

            messages.success(request, "جلسات با موفقیت اضافه شد", 'success')
            return redirect('cart')


# this view deletes teacher's plan for creating a new one


class DeleteTeacherPlanView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def get(self, request, plan_id):
        if request.user.is_teacher:
            teacher_plan = TeacherPlan.objects.get(id=plan_id)
            plan_times = PlanTime.objects.filter(teacherplan=teacher_plan)
            teacher_times = TeacherTime.objects.filter(teacher=request.user).filter(is_reserved=False)
            for t_time in teacher_times:
                for p_time in plan_times:
                    if t_time.week_day == p_time.week_day and t_time.start == p_time.start:
                        t_time.delete()
            teacher_plan.delete()
            messages.success(request, "برنامه شما با موفقیت حذف شد", 'success')
            return redirect('time_checkbox')
        else:
            return redirect('home')


class TeacherTimeReportView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def get(self, request, teacher_time_id):
        if request.user.is_teacher:
            t_time = TeacherTime.objects.get(id=teacher_time_id)
            context = {'teacher_time': t_time}
            return render(request, 'courses/teacher_time_report.html', context)
        else:
            return redirect('home')

    def post(self, request, teacher_time_id):
        if request.user.is_teacher:
            teacher_time_report = request.POST.get('report')
            teacher_time = TeacherTime.objects.get(id=teacher_time_id)
            teacher_time.report = teacher_time_report
            teacher_time.save()
            return redirect('account_details')
        else:
            return redirect('home')