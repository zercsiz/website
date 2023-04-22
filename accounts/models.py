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
    description = models.TextField(verbose_name="Description", max_length=1000, null=True, blank=True)
    skill_choices = {('g', 'زبان آلمانی'), ('e', 'زبان انگلیسی')}
    skill = models.CharField(verbose_name="Skill", max_length=200, null=True, blank=True, choices=skill_choices)
    slug = models.SlugField(null=True, blank=True, max_length=300, unique=True, allow_unicode=True)

    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    # overrides save function , this is commented because i dont know how to farsi slug
    def save(self, *args, **kwargs):
        if self.is_teacher:
            try:
                slug = "-".join([self.skill, self.first_name, self.last_name])
                print(slug)
            except TypeError or ValueError:
                slug = None
            if slug:
                self.slug = slugify(slug, allow_unicode=True)
        super().save()

    def __str__(self):
        if self.is_superuser:
            return f"Admin | {self.username} | {self.phone_number} | {self.email}"
        elif self.is_student:
            return f"Student | {self.username} | {self.email}"
        else:
            return f"Teacher | {self.first_name} {self.last_name} | {self.skill}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_lable):
        return True

    def get_absolute_url(self):
        return reverse('teacher_details', args=(self.id, self.slug))
