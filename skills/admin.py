from django.contrib import admin
from . import models


@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category',)