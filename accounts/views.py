from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from courses.models import *


class UserRegistrationView(View):
    def post(self, request):
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # phone_number = form.cleaned_data.get('phone_number')
            # raw_password = form.cleaned_data.get('password')
            # account = authenticate(phone_number=phone_number, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            form = forms.RegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def get(self, request):
        form = forms.RegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = forms.UserLoginForm(request.POST or None)
            if form.is_valid():
                user = form.login(request)
                if user:
                    login(request, user)
                    return redirect('home')
            return render(request, 'accounts/login.html', {'form': form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = forms.UserLoginForm()
            return render(request, 'accounts/login.html', {'form': form})



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return redirect('home')


class AccountInfoView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def get(self, request):
        if request.user.is_teacher:
            context = {}
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

    def post(self, request):
        form = forms.AccountEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.error(request, "اطلاعات شما با موفقیت تغییر کرد.", 'success')
            return redirect('account_details')
        return render(request, 'accounts/account_edit.html', {'form': form})

    def get(self, request):
        form = forms.AccountEditForm(instance=request.user)
        return render(request, 'accounts/account_edit.html', {'form': form})
