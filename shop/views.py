from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class CartView(View):
    def get(self, request):
        return render(request, 'shop/cart.html')
