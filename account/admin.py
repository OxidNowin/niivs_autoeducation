from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Subdivision
from .forms import UserChangeForm, UserCreationForm

from string import ascii_letters, digits


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'name', 'subdivision', 'receipt', 'is_active', 'is_admin', 'is_superuser')
    list_filter = ('is_admin', 'is_active', 'is_superuser')
    fieldsets = (
        ('Информация об аккаунте', {'fields': ('email', 'password')}),
        ('Персональная информация', {
            'fields': (
					'name', 
                    'subdivision', 
                    'education', 
                    'education_profile', 
                    'receipt',
                    )
            }),
        ('Привилегии', {'fields': ('is_admin', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        ('Информация об аккаунте', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)}
        ),
        ('Персональная информация', {
            'fields': (
                    'name', 
                    'subdivision', 
                    'education', 
                    'education_profile', 
                    'receipt',
                    )

        }),
        ('Права доступа:', {
            'fields': (
                'is_superuser',
                'is_active',
                )
            }),
    )
    search_fields = ('email',)
    ordering = ('name', 'subdivision',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Subdivision)
admin.site.unregister(Group)