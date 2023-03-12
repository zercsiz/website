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
