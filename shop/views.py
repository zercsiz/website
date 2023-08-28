from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import *


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            order = request.user.order.get(complete=False)
            items = OrderItem.objects.filter(order=order)
            orderItems = order.order_orderItems.all()
            order.total = sum([item.teacherTime.price for item in orderItems])
            order.save()
        except Order.DoesNotExist:
            order = None
            items = None

        context = {'order_items': items, 'order': order}
        return render(request, 'shop/cart.html', context)


class removeItem(LoginRequiredMixin, View):
    def get(self, request, item_id):
        order_item = OrderItem.objects.get(id=item_id)
        order_item.delete()
        messages.success(request, "کلاس با موفقیت حذف شد", 'success')
        return redirect('shop:cart')


class OrderCompleteView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # login Url for LoginRequiredMixin

    def get(self, request, order_id):
        ## this whole section is gonna change because we want to complete the orders by hand in admin panel
        if not request.user.username or not request.user.first_name or not request.user.last_name or not request.user.phone_number:
            messages.error(request, "لطفا اطلاعات کاربری خود را در قسمت ویرایش اطلاعات کاربری کامل کنید", 'danger')
            return redirect('accounts:account_details')
        else:
            try:
                order = Order.objects.get(id=order_id)
                order.complete = True
                order.save()
                order_items = order.order_orderItems.all()
                ## already_reserved is because we want to show an error is some teacherTimes were already reserved before user reserve them
                already_reserved = False
                for item in order_items:
                    if not item.teacherTime.is_reserved:
                        item.teacherTime.student = request.user
                        item.teacherTime.is_reserved = True
                        item.teacherTime.save()
                    else:
                        already_reserved = True
                if already_reserved == True:
                    messages.error(request, "تعدادی از جلسات انتخابی از قبل رزور شده اند", 'danger')
                    return redirect('accounts:account_details')
                else:
                    messages.success(request, "جلسات انتخابی با موفقیت رزرو شدند", 'success')
                    return redirect('accounts:account_details')
            except Order.DoesNotExist:
                messages.success(request, "سفارش یافت نشد", 'danger')
                return redirect('shop:cart')

                
class UserOrdersView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        try:
            orders = Order.objects.filter(student=request.user)
        except:
            orders = None
        context = {'orders': orders}
        return render(request, 'shop/user_orders.html', context)
                


