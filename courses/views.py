from django.shortcuts import render, redirect
from .models import *
from shop.models import *
from datetime import date, timedelta, datetime
from accounts.models import Account
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages



class CreateTime(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        # this function converts weekday number to farsi weekday names because we need to show the user persian week days
        def week_day_convert(day_number):
            # here shanbe is 5
            day_list = ['دوشنبه','سه شنبه','چهارشنبه','پنجشنبه','جمعه','شنبه','یکشنبه',]
            return day_list[day_number]

        # this function adds 1:30 to start time because all courses have a length of 1:30
        def calculate_endtime(start):
            hour = int(start[0:2])
            minute = int(start[3:])
            end = timedelta(hours=hour, minutes=minute) + timedelta(hours=1, minutes=30)
            return end

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

        return redirect('accounts:account_details')

    def get(self, request):
        try:
            plan = request.user.plan.get()
            context = {'plan': plan}
        except TeacherPlan.DoesNotExist:
            context = {'plan': None}

        return render(request, 'courses/time_checkbox.html', context)


class TeacherDetails(LoginRequiredMixin, View):
    def get(self, request, teacher_id, teacher_slug):
        teacher = Account.objects.get(id=teacher_id)
        week_days = ("شنبه", "یکشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنجشنبه", "جمعه",)
        hours = ("09:00", "10:30", "12:00", "13:30", "15:00", "16:30", "18:00", "19:30")
        try:
            teacher_plan = teacher.plan.get()
            plan_times = teacher_plan.teacherPlan_planTimes.all()
            context = {
                'teacher': teacher,
                'plan_times': plan_times,
                'week_days': week_days,
                'hours': hours
            }
        except TeacherPlan.DoesNotExist:
            teacher_plan = None
            context = {
                'teacher': teacher,
            }
        return render(request, 'courses/teacher_details.html', context)

    def post(self, request, teacher_id, teacher_slug):

        # checks if user is trying to reserve their own times because they shouldnt be able to do that
        if request.user.id == teacher_id:
            messages.error(request, "اساتید امکان رزرو کلاس های خود را ندارند.", 'danger')
            return redirect('courses:teacher_details', teacher_id, teacher_slug)
        try:
            order = request.user.student_orders.get(status='pending')
            messages.error(request, "کاربر عزیز شما یک سفارش در حال بررسی دارید", 'danger')
            return redirect('courses:teacher_details', teacher_id, teacher_slug)
        except:

            # this checks if user specified a start date and if they didnt, sets the start date today()
            try:
                start_date = datetime.strptime(request.POST.get('start_date'), "%Y-%m-%d").date()
            except:
                ## because we want to have time to evaluate users order and imform the teacher we want 7 days time
                start_date = date.today() + timedelta(days=7)
            
            # create order for student, it checks if there is an uncompleted order because we dont want to create an order everytime
            try:
                order = request.user.student_orders.get(status='incomplete')
            except Order.DoesNotExist:
                teacher = Account.objects.get(id=teacher_id)
                session_number = request.POST.get('session_number')
                order = Order.objects.create(student=request.user, sessions_number=int(session_number), start_date=start_date, teacher=teacher)
                order.save()

            plan_times_ids = request.POST.getlist('p_time_id')

            plan_times_list = []
            for i in plan_times_ids:
                planTime = PlanTime.objects.get(id=i)
                order.planTimes.add(planTime)
                order.save()
                plan_times_list.append(planTime)

            ## to calculate the total amount for order
            order.total = plan_times_list[0].teacherplan.price * order.sessions_number
            order.save()
            print(order.planTimes.all())


            # teacher = Account.objects.get(id=teacher_id)
            # plan = teacher.plan.get()

            
            # order_items = []

            # end_date = date(2024, 12, 1)

            # for single_date in daterange(start_date, end_date):
            #     jdate = date2jalali(single_date).strftime("%Y-%m-%d")
            #     for planTime in plan_times:
            #         if single_date.weekday() == planTime.week_day_number:
            #             # this checks whether the date and time is reserved and if it is, skips the day
            #             ## here "gdate" is gregorian date and "date" is jalali
            #             t_time, created = TeacherTime.objects.get_or_create(date=jdate, gdate=single_date.strftime("%Y-%m-%d"),
            #                         week_day=planTime.week_day, start=planTime.start, end=planTime.end, price=plan.price,
            #                         google_meet_link=plan.google_meet_link, teacher=teacher)
            #             if t_time.is_reserved:
            #                 break
            #             else:
            #                 item = OrderItem.objects.get_or_create(teacherTime=t_time, order=order)
            #                 order_items.append(item)
                            
            #         if len(order_items) == int(session_number):
            #             break
            #     if len(order_items) == int(session_number):
            #         break

            messages.success(request, "جلسات با موفقیت اضافه شد", 'success')
            return redirect('shop:cart')


# this view deletes teacher's plan for creating a new one

class DeleteTeacherPlanView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher or not kwargs['plan_id']:
            return redirect('home:home')
        
        # because we dont want to let the teacher delete his plan when he has pending or incomplete orders related to him
        teacher_orders = request.user.teacher_orders.all()
        for item in teacher_orders:
            if item.status == "incomplete" or item.status == "pending":
                messages.error(request, "در حال حاضر امکان حدف برنامه وجود ندارد", 'danger')
                return redirect('courses:time_checkbox')
            
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, plan_id):
        teacher_plan = TeacherPlan.objects.get(id=plan_id)
        plan_times = teacher_plan.teacherPlan_planTimes.all()
        teacher_times = request.user.teacher_teacherTimes.filter(is_reserved=False)
        for t_time in teacher_times:
            for p_time in plan_times:
                if t_time.week_day == p_time.week_day and t_time.start == p_time.start:
                    t_time.delete()
        teacher_plan.delete()
        messages.success(request, "برنامه شما با موفقیت حذف شد", 'success')
        return redirect('courses:time_checkbox')


class TeacherTimeReportView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def setup(self, request, *args, **kwargs):
        # gets a particular teacher time
        self.teacher_time_instance = TeacherTime.objects.get(id=kwargs['teacher_time_id'])

        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, teacher_time_id):
        context = {'teacher_time': self.teacher_time_instance}
        return render(request, 'courses/teacher_time_report.html', context)

    def post(self, request, teacher_time_id):
        teacher_time_report = request.POST.get('report')
        teacher_time = self.teacher_time_instance
        teacher_time.report = teacher_time_report
        teacher_time.save()
        return redirect('accounts:account_details')


class GoogleMeetLinkTutorialView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'courses/google_meet_link_tutorial.html')