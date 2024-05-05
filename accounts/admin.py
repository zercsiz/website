from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class AccountAdmin(UserAdmin):
    list_display = ('username',
                    'phone_number',
                    'email',
                    'date_joined',
                    'last_login',
                    'is_admin',
                    'is_student',
                    'is_teacher')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(models.Account, AccountAdmin)
