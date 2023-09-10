from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models


@receiver(post_save, sender=models.Order)
def orderComplete(sender, instance, **kwargs):
    if sender.objects.get(id=instance.id).status == 'complete':
        order = sender.objects.get(id=instance.id)
        orderItems = order.order_orderItems.all()
        for orderItem in orderItems:
            if not orderItem.teacherTime.is_reserved:
                orderItem.teacherTime.student = order.student
                orderItem.teacherTime.is_reserved = True
                orderItem.teacherTime.save()

@receiver(post_save, sender=models.Order)
def orderNotComplete(sender, instance, **kwargs):
    if sender.objects.get(id=instance.id).status == 'incomplete':
        order = sender.objects.get(id=instance.id)
        orderItems = order.order_orderItems.all()
        for orderItem in orderItems:
            if orderItem.teacherTime.student == order.student:
                orderItem.teacherTime.student = None
                orderItem.teacherTime.is_reserved = False
                orderItem.teacherTime.save()
