from django.db import models
from django.conf import settings
from courses.models import TeacherTime


class Order(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="Student")
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=250, null=True)
    total = models.BigIntegerField(null=True)

    def __str__(self):
        return f"completed:{self.complete}"


class OrderItem(models.Model):
    teacherTime = models.ForeignKey(TeacherTime, on_delete=models.CASCADE, null=True, blank=True, related_name="TeacherTime")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="Order")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacherTime} - id = {self.id}"