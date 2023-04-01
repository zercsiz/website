from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels


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
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    date = jmodels.jDateField(null=True)
    week_day = models.CharField(max_length=50, null=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    is_reserved = models.BooleanField(default=False)
    google_meet_link = models.CharField(null=True, max_length=250)

    def __str__(self):
        return f"{self.date} | {self.start} | {self.end} | Reserve Status = {self.is_reserved}"
