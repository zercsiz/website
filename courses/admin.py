from django.contrib import admin
from . import models


@admin.register(models.Course)
class PlanTimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'days', 'hour', 'created', 'price')
    search_fields = ('title',)
