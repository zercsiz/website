from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("Phone number is required!")
        user = self.model(
            phone_number=phone_number,
            password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(
            phone_number=phone_number,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_student = False
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    phone_number = models.CharField(verbose_name='Phone Number', max_length=11, unique=True)
    username = models.CharField(max_length=250, unique=True, null=True)
    email = models.CharField(verbose_name='Email', max_length=250, unique=True, null=True)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        if self.is_superuser:
            return f"Admin | {self.username} | {self.phone_number} | {self.email}"
        elif self.is_student:
            return f"Student | {self.username} | {self.phone_number} | {self.email}"
        else:
            return f"Teacher | {self.username} | {self.phone_number} | {self.email}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_lable):
        return True

