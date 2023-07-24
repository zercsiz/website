from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from accounts.models import Account
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="", max_length=250, required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'آدرس ایمیل'}))
    password1 = forms.CharField(label="", max_length=250, required=True,
                             widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))

    class Meta:
        model = Account
        fields = ('email', 'password1')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['password1'].help_text = None
        self.fields['email'].help_text = None

    def clean_email(self):
        email = self.cleaned_data['email']
        user = Account.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError('حساب کاربری با این ایمیل وجود دارد.', code="exists")
        return email


class UserLoginForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

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
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'email', 'skill', 'description')
        if not Account.is_teacher:
            exclude = ('skill', 'description')
        labels = {
            'username': _('نام کاربری'),
            'phone_number': _('شماره همراه'),
            'email': _('ایمیل'),
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'skill': _('مهارت'),
            'description': _('توضیحات'),
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control my-3'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'skill': forms.Select(attrs={'class': 'form-control my-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control my-3', 'rows': '8', 'cols': '50', 'style': "resize: none"}),
        }
        def __init__(self, *args, **kwargs):
            super(AccountEditForm, self).__init__(*args, **kwargs)
            self.fields.all.required = True
            
            
        


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
