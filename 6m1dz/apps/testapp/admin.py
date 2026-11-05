from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_verified', 'is_active')

    list_filter = ('role', 'is_verified', 'is_active')

    search_fields = ('email', 'username')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
          'Персональные данные',
          {'fields': ('first_name', 'last_name', 'email', 'bio', 'birth_date')},
        ),
        (
           'Права доступа и роли',
           {
                'fields': (
                    'role',
                    'is_verified',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'role',
                    'is_verified',
                ),
            },
        ),
    )