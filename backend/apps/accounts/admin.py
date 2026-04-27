from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_admin', 'is_superuser', 'institut']
    list_filter = ['is_admin', 'is_superuser', 'institut']
    fieldsets = UserAdmin.fieldsets + (
        ('Rôle plateforme', {'fields': ('is_admin', 'institut')}),
    )
