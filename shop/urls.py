from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name="cart"),
    path('update_item/', views.updateItem, name="update_item")
]