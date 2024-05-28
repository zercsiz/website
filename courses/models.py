from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels
from django.urls import reverse
from django.contrib.auth import get_user_model




class Course(models.Model):

    title = models.CharField(max_length=250)
    description = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(verbose_name="Start Date")
    days = models.CharField(max_length=200)
    hour = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True, upload_to='images/courses/')
    price = models.BigIntegerField(null=True)
    link = models.CharField(max_length=3000, null=True, blank=True)

    students = models.ManyToManyField(get_user_model(), blank=True, related_name="courses")

    def __str__(self):
        return f"{self.title} | Start Date:{self.start_date} | {self.description[:60]}... | Days:{self.created} | Hour:{self.edited}"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def get_absolute_url(self):
        return reverse('courses:course_details', args=(self.id,))

