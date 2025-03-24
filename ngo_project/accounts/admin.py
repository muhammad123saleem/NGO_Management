from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Show email and name in the list display
    list_display = ('email', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    # Organize fields in the change (edit) page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'mobile_no', 'address', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to display when adding a new user via the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'name', 'mobile_no', 'address', 'role', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('email', 'name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
