from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from courses.models import *
from accounts.models import *


class UserRegistrationView(View):
    form_class = forms.RegistrationForm
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "حساب کاربری شما با موفقیت ایجاد شد. برای رزرو کلاس به صفحه اصلی مراجعه کنید.", 'success')
            login(request, user)
            return redirect('accounts:account_details')
        return render(request, 'accounts/register.html', {'form': form})

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    form_class = forms.UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return redirect('home:home')
        return render(request, 'accounts/login.html', {'form': form})

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        return redirect('home:home')
    

class AccountInfoView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if request.user.is_teacher:
            context = {}
            if not request.user.first_name or not request.user.last_name or not request.user.skill or not request.user.description:
                context['uncomplete_info'] = True
            else:
                context['uncomplete_info'] = False
            # week days in farsi for teacher plan
            w_days = ("شنبه", "یکشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنجشنبه", "جمعه", )
            context['week_days'] = w_days

            try:
                teacher_plan = request.user.plan.get()
                p_times = teacher_plan.teacherPlan_planTimes.all()
                context['plan_times'] = p_times
            except:
                context['plan_times'] = None
            try:
                ## teacher_teacherTimes means times when user is teacher, and student_teacherTime means times when user is student
                teacher_time_as_teacher_list = request.user.teacher_teacherTimes.filter(is_reserved=True).order_by('gdate')
                context['teacher_times_as_teacher'] = teacher_time_as_teacher_list
            except:
                context['teacher_times_as_teacher'] = None
            try:
                teacher_time_as_student_list = request.user.student_teacherTimes.filter(is_reserved=True).order_by('gdate')
                context['teacher_times_as_student'] = teacher_time_as_student_list
            except:
                context['teacher_times_as_student'] = None
        else:
            context = {}
            try:
                teacher_time_as_student_list = request.user.student_teacherTimes.filter(is_reserved=True).order_by('gdate')
                context['teacher_times_as_student'] = teacher_time_as_student_list
            except:
                context['teacher_times_as_student'] = None
                
        return render(request, 'accounts/account_information.html', context)


class AccountEditView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin
    form_class = forms.AccountEditForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات شما با موفقیت تغییر کرد.", 'success')
            return redirect('accounts:account_details')
        return render(request, 'accounts/account_edit.html', {'form': form})

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, 'accounts/account_edit.html', {'form': form})
