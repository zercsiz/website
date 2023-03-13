from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from accounts.models import Account


class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=11, help_text="Required. Please enter a valid phone number")

    class Meta:
        model = Account
        fields = ("username", "phone_number", "password1", "password2")


class UserLoginForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('phone_number', 'password')

    def clean(self):
        if self.is_valid():
            phone_number = self.cleaned_data['phone_number']
            password = self.cleaned_data['password']
            if not authenticate(phone_number=phone_number, password=password):
                raise forms.ValidationError("Invalid Login!")


class AccountEditForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', 'phone_number', 'email')

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)

            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" already exists!' % account.username)

    def clean_phone_number(self):
        if self.is_valid():
            phone_number = self.cleaned_data['phone_number']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(phone_number=phone_number)

            except Account.DoesNotExist:
                return phone_number
            raise forms.ValidationError('Phone number "%s" already exists!' % account.phone_number)

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)

            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email number "%s" already exists!' % account.email)
