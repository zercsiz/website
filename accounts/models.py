from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.text import slugify
from django.urls import reverse


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email address is required!")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_student = True
        user.is_teacher = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    phone_number = models.CharField(verbose_name='Phone Number', max_length=11, unique=True, null=True, blank=True)
    username = models.CharField(max_length=250, unique=True, null=True, blank=True)
    email = models.CharField(verbose_name='Email', max_length=250, unique=True, null=True)
    first_name = models.CharField(verbose_name="First Name", max_length=200, null=True, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=200, null=True, blank=True)
    

    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_lable):
        return True

    def get_absolute_url(self):
        return reverse('courses:teacher_details', args=(self.id, self.slug))
