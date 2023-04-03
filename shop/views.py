from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json
from .models import *


class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            student = request.user
            order, created = Order.objects.get_or_create(student=student, complete=False)
            items = OrderItem.objects.filter(order=order)
        else:
            items = []
        context = {'items': items}
        return render(request, 'shop/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    teacherTimeId = data['teacherTimeId']
    action = data['action']

    print('Action', action)
    print('teacherTimeId', teacherTimeId)
    return JsonResponse("Item was added", safe=False)