from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json


class CartView(View):
    def get(self, request):
        return render(request, 'shop/cart.html')


def updateItem(request):
    return JsonResponse("Item was added", safe=False)