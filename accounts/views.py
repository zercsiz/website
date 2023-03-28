from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from courses.models import TeacherTime
from django.views import View


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


def account_details_view(request):
    teacher_time_list = TeacherTime.objects.all()
    context = {'teacher_time': teacher_time_list}
    return render(request, 'accounts/account_information.html', context)


def account_edit_view(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    if request.POST:
        form = forms.AccountEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account_details')
    else:
        form = forms.AccountEditForm(
            initial={
                "username": request.user.username,
                "phone_number": request.user.phone_number,
                "email": request.user.email,
            }
        )
    return render(request, 'accounts/account_edit.html', {'form': form})
















