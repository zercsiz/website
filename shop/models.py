from django.db import models
from django.conf import settings


class Order(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="student_orders")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="teacher_orders")

    planTimes = models.ManyToManyField("courses.PlanTime")

    start_date = models.DateField(null=True, blank=True)
    sessions_number = models.IntegerField(null=True, blank=True)

    date_ordered = models.DateTimeField(auto_now_add=True)

    status_choices = {('complete', 'complete'), ('pending', 'pending'), ('incomplete', 'incomplete')}

    status = models.CharField(choices=status_choices, max_length=100, null=True, blank=True, default="incomplete")
    total = models.BigIntegerField(null=True)

    def __str__(self):
        return f"{self.student} - status:{self.status}"


class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name="Transaction")

    date = models.CharField(max_length=100, null=True, blank=True)
    hour = models.CharField(max_length=100, null=True, blank=True)
    minute = models.CharField(max_length=100, null=True, blank=True)

    dateIssued = models.DateTimeField(auto_now_add=True)

    amount = models.FloatField(null=True, blank=True)
    card4Digits = models.CharField(max_length=4, null=True, blank=True)
    transactionId = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.amount} - {self.date} - {self.hour}"