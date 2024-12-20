from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name="cart"),
    path('remove_item/<int:item_id>/', views.removeItem.as_view(), name="remove_item"),
    path('order_complete/<int:order_id>', views.OrderCompleteView.as_view(), name="order_complete"),
    path('orders/', views.UserOrdersView.as_view(), name='user_orders'),
    path('transaction_info/<int:order_id>', views.TransactionInfoView.as_view(), name="transactionInfo"),
]