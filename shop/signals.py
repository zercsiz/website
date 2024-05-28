from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models as shopModels
from courses import models as coursesModels



@receiver(post_save, sender=shopModels.Order)
def orderComplete(sender, instance, **kwargs):
    order = sender.objects.get(id=instance.id)
    if order.status == 'c':
        course = coursesModels.Course.objects.get(id=order.courseId)
        course.students.add(order.student)
        course.save()
        

    


      