from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'role','is_staff', 'is_active')
    list_filter = ('role','is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role',)}),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active','role')
            },
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
