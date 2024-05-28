from typing import Any
from django import http
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
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "حساب کاربری شما با موفقیت ایجاد شد. برای رزرو کلاس به صفحه اصلی مراجعه کنید.", 'success')
            login(request, user)
            return redirect('accounts:user_profile')
        
        return render(request, 'accounts/register.html', {'form': form})

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    form_class = forms.UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
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
                if self.next:
                    return redirect(self.next)
                
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
    

class UserProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def setup(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.courses_instance = request.user.courses.all()
        return super().setup(request, *args, **kwargs)
    
    def get(self, request):
        context = {'courses': self.courses_instance}        
        return render(request, 'accounts/user_profile.html', context)


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
