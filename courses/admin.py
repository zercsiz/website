from django.contrib import admin
from . import models


admin.site.register(models.Course)

@admin.register(models.PlanTime)
class PlanTimeAdmin(admin.ModelAdmin):
    list_display = ('teacherplan', 'week_day', 'week_day_number', 'start', 'end')
    search_fields = ('week_day', 'start',)
    raw_id_fields = ('teacherplan',)

@admin.register(models.TeacherPlan)
class TeacherPlanAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'google_meet_link', 'price')
    search_fields = ('teacher',)
    raw_id_fields = ('teacher',)


@admin.register(models.TeacherTime)
class TeacherTimeAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'date', 'start', 'is_reserved', 'student')
    list_filter = ('is_reserved', 'teacher', 'student')
    search_fields = ('teacher', 'student')
    raw_id_fields = ('teacher', 'student')

