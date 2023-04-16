from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels
from datetime import date, datetime, time
import time


languages = [
    ('e', 'English'),
    ('g', 'German')
]


class Course(models.Model):

    title = models.CharField(max_length=250)
    description = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(verbose_name="Start Date")
    days = models.CharField(max_length=200)
    hour = models.CharField(max_length=200)
    language = models.CharField(max_length=1, choices=languages)

    def __str__(self):
        return f"{self.title} | Language:{self.language} | Start Date:{self.start_date} | {self.description[:60]}... | Days:{self.created} | Hour:{self.edited}"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class TeacherTime(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="teacher")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="student")
    date = jmodels.jDateField(null=True)
    gdate = models.DateField(null=True)
    week_day = models.CharField(max_length=50, null=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    price = models.BigIntegerField(null=True, blank=True)
    is_reserved = models.BooleanField(default=False)
    google_meet_link = models.CharField(null=True, max_length=250)
    report = models.TextField(null=True)

    def __str__(self):
        return f"{self.gdate} | {self.start} | Reserve Status = {self.is_reserved}"


class TeacherPlan(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="Teacher")
    google_meet_link = models.CharField(null=True, max_length=250)
    price = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.teacher.email}"


class PlanTime(models.Model):
    teacherplan = models.ForeignKey(TeacherPlan, on_delete=models.CASCADE, null=True, blank=True, related_name="TeacherPlan")
    week_day = models.CharField(max_length=50, null=True)
    week_day_number = models.IntegerField(null=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
