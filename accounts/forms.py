from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from accounts.models import Account
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email, EmailValidator
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="", max_length=250, required=True, widget=forms.EmailInput())
    password1 = forms.CharField(label="", max_length=250, required=True, widget=forms.PasswordInput())

    captcha = CaptchaField()

    class Meta:
        model = Account
        fields = ('email', 'password1')

        # to override djangos error messages
        error_messages = {
            'email': {
                'invalid': 'لطفا ایمیل معتبر وارد کنید',
                'unique': 'این ایمیل قبلا استفاده شده است',
                'required': 'ایمیل الزامی است',
            },
        }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        # password repeat field remove
        # del self.fields['password2']

        self.fields['password1'].help_text = "رمز عبور شما باید حداقل 8 کرکتر باشد"

    def clean_email(self):
        email = self.cleaned_data['email']
        try: 
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('لطفا ایمیل معتبر وارد کنید', code="invalid")

        user = Account.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError('این ایمیل قبلا استفاده شده است', code="unique")
          
        return email
    
    def clean_password1(self):
        password = self.cleaned_data['password1']
        
        return password

class UserLoginForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    captcha = CaptchaField()

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if not user or not user.is_active:
                # massage for invalid login
                raise forms.ValidationError("نام کاربری یا رمز عبور اشتباه است.")
            return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'email')
        labels = {
            'username': _('نام کاربری'),
            'phone_number': _('شماره همراه'),
            'email': _('ایمیل'),
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control my-3'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control my-3'}),
        }        

    def clean_username(self):
        username = self.cleaned_data['username']
        if username and self.is_valid():
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" already exists!' % account.username)
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if phone_number and self.is_valid():
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(phone_number=phone_number)
            except Account.DoesNotExist:
                return phone_number
            raise forms.ValidationError('Phone number "%s" already exists!' % account.phone_number)
        return phone_number
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if email and self.is_valid():
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" already exists!' % account.email)
        return email
