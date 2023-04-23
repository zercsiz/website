from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import *


class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            student = request.user
            try:
                order = Order.objects.get(student=student, complete=False)
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


class removeItem(LoginRequiredMixin, View):
    def get(self, request, item_id):
        order_item = OrderItem.objects.get(id=item_id)
        order_item.teacherTime.delete()
        order_item.delete()
        messages.success(request, "کلاس با موفقیت حذف شد", 'success')
        return redirect('cart')


class OrderCompleteView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.complete = True
            order.save()
        except Order.DoesNotExist:
            order = None
        if order:
            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                item.teacherTime.student = request.user
                item.teacherTime.is_reserved = True
                item.teacherTime.save()
            return redirect('account_details')
        else:
            messages.success(request, "سفارش یافت نشد", 'danger')
            return redirect('cart')


