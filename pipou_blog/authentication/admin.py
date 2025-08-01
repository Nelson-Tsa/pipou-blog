from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'first_name', 'last_name', 'date_joined')
    ordering = ('email',)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Informations personnelles"), {"fields": ("first_name", "last_name", "biography", "profile_picture")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Dates importantes"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "first_name", "last_name"),
        }),
    )

    search_fields = ("email", "first_name", "last_name")
