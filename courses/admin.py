from django.contrib import admin
from . import models


admin.site.register(models.Course)
admin.site.register(models.TeacherPlan)
admin.site.register(models.PlanTime)


@admin.register(models.TeacherTime)
class TeacherTimeAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'date', 'start', 'is_reserved', 'student')
    list_filter = ('is_reserved', 'teacher', 'student')
    search_fields = ('teacher', 'student')
    raw_id_fields = ('teacher', 'student')

