from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from accounts.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=250, help_text="Required. Please enter a valid email address")

    class Meta:
        model = Account
        fields = ('email', 'password1')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['password1'].help_text = None
        self.fields['email'].help_text = None


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
                raise forms.ValidationError("نام کاربری یا رمز ورود اشتباه است.")
            return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user


class AccountEditForm(forms.ModelForm):
    username = forms.CharField(label="نام کاربری", widget=forms.TextInput(attrs={'class': 'form-control my-3'}))
    phone_number = forms.CharField(label="شماره تلفن همراه", widget=forms.TextInput(attrs={'class': 'form-control my-3'}), required=True, max_length=11)
    email = forms.EmailField(label="آدرس ایمیل", widget=forms.EmailInput(attrs={'class': 'form-control my-3'}), required=True)
    first_name = forms.CharField(label="نام", widget=forms.TextInput(attrs={'class': 'form-control my-3'}), required=True)
    last_name = forms.CharField(label="نام خانوادگی", widget=forms.TextInput(attrs={'class': 'form-control my-3'}), required=True)
    skill_choices = {('g', 'زبان آلمانی'), ('e', 'زبان انگلیسی')}
    skill = forms.ChoiceField(label="مهارت", required=True, choices=skill_choices, widget=forms.Select(attrs={'class': 'form-control my-3'}))
    description = forms.CharField(label="توضیحات", widget=forms.Textarea(attrs={'class': 'form-control my-3'}), required=True)

    class Meta:
        model = Account
        fields = ('username', 'phone_number', 'email', 'first_name', 'last_name', 'skill', 'description')


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
