from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
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
            teacher = request.user
            t_plan = TeacherPlan.objects.get(teacher=teacher)
            p_time = PlanTime.objects.filter(teacherplan=t_plan)
            teacher_time_list = TeacherTime.objects.all()
            context = {'teacher_time': teacher_time_list,
                       'plan_times': p_time}
        else:
            context = {}
        return render(request, 'accounts/account_information.html', context)


class AccountEditView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def post(self, request):
        form = forms.AccountEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account_details')
        return render(request, 'accounts/account_edit.html', {'form': form})

    def get(self, request):
        form = forms.AccountEditForm(
            initial={
                "username": request.user.username,
                "phone_number": request.user.phone_number,
                "email": request.user.email,
            }
        )
        return render(request, 'accounts/account_edit.html', {'form': form})
















