from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models
from datetime import timedelta, date
from jalali_date import date2jalali
from courses import models as coursesModels
from shop import models as shopModels


@receiver(post_save, sender=models.Order)
def orderComplete(sender, instance, **kwargs):
    if sender.objects.get(id=instance.id).status == 'complete':


        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)


        order = sender.objects.get(id=instance.id)
        plan_times = order.planTimes.all()

        teacher = plan_times[0].teacherplan.teacher
        plan = teacher.plan.get()

        start_date = order.start_date
        order_items = []
        end_date = date(2024, 12, 1)

        for single_date in daterange(start_date, end_date):
            jdate = date2jalali(single_date).strftime("%Y-%m-%d")
            for planTime in plan_times:
                if single_date.weekday() == planTime.week_day_number:
                    # this checks whether the date and time is reserved and if it is, skips the day
                    ## here "gdate" is gregorian date and "date" is jalali
                    t_time, created = coursesModels.TeacherTime.objects.get_or_create(date=jdate, gdate=single_date.strftime("%Y-%m-%d"),
                                week_day=planTime.week_day, start=planTime.start, end=planTime.end, price=plan.price,
                                google_meet_link=plan.google_meet_link, teacher=teacher, student=order.student, order=order)
                    if t_time.is_reserved:
                        break
                    else:
                        order_items.append(t_time)
                        
                if len(order_items) == order.sessions_number:
                    break
            if len(order_items) == order.sessions_number:
                break

        for t_time in order_items:
            t_time.is_reserved = True
            t_time.save()


        # orderItems = order.order_orderItems.all()
        # for orderItem in orderItems:
        #     if not orderItem.teacherTime.is_reserved:
        #         orderItem.teacherTime.student = order.student
        #         orderItem.teacherTime.is_reserved = True
        #         orderItem.teacherTime.save()

# @receiver(post_save, sender=models.Order)
# def orderNotComplete(sender, instance, **kwargs):
#     if sender.objects.get(id=instance.id).status == 'incomplete':
#         order = sender.objects.get(id=instance.id)
#         orderItems = order.order_orderItems.all()
#         for orderItem in orderItems:
#             if orderItem.teacherTime.student == order.student:
#                 orderItem.teacherTime.student = None
#                 orderItem.teacherTime.is_reserved = False
#                 orderItem.teacherTime.save()
