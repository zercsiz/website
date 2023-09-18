from django.contrib import admin
from . import models
from courses import models as coursesModels


class TransactionInline(admin.StackedInline):
    model = models.Transaction
    can_delete = False
    readonly_fields = ('order', 'date', 'hour', 'minute', 'dateIssued', 'card4Digits', 'transactionId', 'amount')
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('student', 'date_ordered', 'status', 'total')
    list_filter = ('status',)
    search_fields = ('student',)
    raw_id_fields = ('student',)
    inlines = [TransactionInline]


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('order', 'date', 'hour', 'minute', 'dateIssued', 'card4Digits', 'transactionId', 'amount')
    search_fields = ('transactionId', 'date_issued','order')


