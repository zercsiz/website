from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
import json
from .models import *


class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            student = request.user
            try:
                order = Order.objects.get(student=student)
                items = OrderItem.objects.filter(order=order)
                order.total = sum([item.teacherTime.price for item in items])
                order.save()
            except Order.DoesNotExist:
                order = None
                items = None

        else:
            items = []
            order = {'total': 0}
        context = {'order_items': items, 'order': order}
        return render(request, 'shop/cart.html', context)



def updateItem(request):
    data = json.loads(request.body)
    teacherTimeId = data['teacherTimeId']
    action = data['action']
    student = request.user
    teacherTime = TeacherTime.objects.get(id=teacherTimeId)
    order, created = Order.objects.get_or_create(student=student, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, teacherTime=teacherTime)
    messages.success(request, "کلاس به سبد خرید شما اضافه شد", 'success')
    return JsonResponse("Item was added", safe=False)


class removeItem(View):
    def get(self, request, item_id):
        order_item = OrderItem.objects.get(id=item_id)
        order_item.teacherTime.delete()
        order_item.delete()
        messages.success(request, "کلاس با موفقیت حذف شد", 'success')
        return redirect('cart')
