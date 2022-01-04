from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_fields = ['id']
    list_display = ( 'email', 'first_name', 'last_name', 'is_staff', 'is_active','id',)
    list_filter = ('last_name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('id', 'first_name', 'last_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ( 'email', 'first_name', 'last_name',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
