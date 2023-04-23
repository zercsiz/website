from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name="cart"),
    path('remove_item/<int:item_id>/', views.removeItem.as_view(), name="remove_item"),
    path('order_complete/<int:order_id>', views.OrderCompleteView.as_view(), name="order_complete")
]