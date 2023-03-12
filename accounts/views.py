from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout


def user_registration_view(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            phone_number = form.cleaned_data.get('phone_number')
            raw_password = form.cleaned_data.get('password')
            account = authenticate(phone_number=phone_number, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            form = forms.RegistrationForm()
    else:
        form = forms.RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            phone_number = request.POST['phone_number']
            password = request.POST['password']
            user = authenticate(phone_number=phone_number, password=password)

            if user:
                login(request, user)
                return redirect('home')

    else:
        form = forms.UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
