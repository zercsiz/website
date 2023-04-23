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
            messages.success(request, "حساب کاربری شما با موفقیت ایجاد شد.", 'success')
            login(request, user)
            return redirect('account_details')
        return render(request, 'accounts/register.html', {'form': form})

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    form_class = forms.UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return redirect('home')
        return render(request, 'accounts/login.html', {'form': form})

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        return redirect('home')
    

class AccountInfoView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if request.user.is_teacher:
            context = {}
            if not request.user.first_name or not request.user.last_name or not request.user.skill or not request.user.description:
                context['uncomplete_info'] = True
            else:
                context['uncomplete_info'] = False
            # week days in farsi for plan
            w_days = ("شنبه", "یکشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنجشنبه", "جمعه", )
            context['week_days'] = w_days

            try:
                t_plan = TeacherPlan.objects.get(teacher=request.user)
            except TeacherPlan.DoesNotExist:
                t_plan = None
            try:
                teacher_time_as_teacher_list = TeacherTime.objects.filter(teacher=request.user).filter(is_reserved=True).order_by('gdate')
            except TeacherTime.DoesNotExist:
                teacher_time_as_teacher_list = None
            try:
                teacher_time_as_student_list = TeacherTime.objects.filter(student=request.user).filter(is_reserved=True).order_by('gdate')
            except TeacherTime.DoesNotExist:
                teacher_time_as_student_list = None

            if t_plan:
                p_time = PlanTime.objects.filter(teacherplan=t_plan)
                context['plan_times'] = p_time
            if teacher_time_as_teacher_list:
                context['teacher_times_as_teacher'] = teacher_time_as_teacher_list
            if teacher_time_as_student_list:
                context['teacher_times_as_student'] = teacher_time_as_student_list

        else:
            context = {}
            try:
                teacher_time_as_student_list = TeacherTime.objects.filter(student=request.user).filter(is_reserved=True)
            except TeacherTime.DoesNotExist:
                teacher_time_as_student_list = None
            if teacher_time_as_student_list:
                context['teacher_times_as_student'] = teacher_time_as_student_list
        return render(request, 'accounts/account_information.html', context)


class AccountEditView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin
    form_class = forms.AccountEditForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات شما با موفقیت تغییر کرد.", 'success')
            return redirect('account_details')
        return render(request, 'accounts/account_edit.html', {'form': form})

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, 'accounts/account_edit.html', {'form': form})
