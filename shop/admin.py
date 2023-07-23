from django.contrib import admin
from . import models

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('student', 'date_ordered', 'complete', 'transaction_id', 'total')
    list_filter = ('complete',)
    search_fields = ('student', 'transaction_id')
    raw_id_fields = ('student',)


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('teacherTime', 'order', 'date_added')
    search_fields = ('order', 'teacherTime')

