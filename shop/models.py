from django.db import models
from django.conf import settings


class Order(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="Student")
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f"{self.student} - {self.transaction_id}"
