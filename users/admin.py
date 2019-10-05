from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin')
    search_fields = ()
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, UserAdmin)
