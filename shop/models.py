from django.db import models
from django.conf import settings
from courses.models import TeacherTime


class Order(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="order")
    date_ordered = models.DateTimeField(auto_now_add=True)

    status_choices = {('complete', 'complete'), ('pending', 'pending'), ('incomplete', 'incomplete')}

    status = models.CharField(choices=status_choices, max_length=100, null=True, blank=True, default="incomplete")
    total = models.BigIntegerField(null=True)

    def __str__(self):
        return f"completed:{self.status}"


class OrderItem(models.Model):
    teacherTime = models.ForeignKey(TeacherTime, on_delete=models.CASCADE, null=True, blank=True, related_name="teacherTime_orderItem")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="order_orderItems")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacherTime} - id = {self.id}"
    

class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name="Transaction")

    date = models.CharField(max_length=100, null=True, blank=True)
    hour = models.CharField(max_length=100, null=True, blank=True)
    minute = models.CharField(max_length=100, null=True, blank=True)

    dateIssued = models.DateTimeField(auto_now_add=True)

    amount = models.FloatField(null=True, blank=True)
    card4Digits = models.CharField(max_length=4, null=True, blank=True)
    transactionId = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.amount} - {self.date} - {self.hour}"