from typing import Any
from django import http
from django.shortcuts import render, redirect
from courses.models import Course
from accounts.models import Account
from django.views import View
from accounts import forms as accountForms
from django.contrib.auth import login
from django.contrib import messages


class HomeView(View):
    form_class = accountForms.RegistrationForm

    def setup(self, request, *args, **kwargs):
        self.teacherListInstance = Account.objects.filter(is_teacher=True).exclude(slug__exact="")[:6]
        self.courseListInstance = Course.objects.all()[:6]
        return super().setup(request, *args, **kwargs)
    
    def get(self, request):
        context = {'courses': self.courseListInstance, "teachers": self.teacherListInstance, 'register_form':self.form_class}

        return render(request, 'home/home.html', context)
    
    def post(self, request):

        context = {'courses': self.courseListInstance, "teachers": self.teacherListInstance, 'register_form':self.form_class}
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "حساب کاربری شما با موفقیت ایجاد شد. برای رزرو کلاس به صفحه اصلی مراجعه کنید.", 'success')
            login(request, user)
            return redirect('accounts:account_details')
        return render(request, 'home/home.html', context)


class PaletteView(View):
    def get(self, request):
        return render(request, 'home/palette.html')
