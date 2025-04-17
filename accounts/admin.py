from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms.models import ModelForm
from django.http import HttpRequest
from .forms import UserCreateForm, UserChangeForm
from .models import User, OtpCode


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm

    fieldsets = (
        ('ChangeUser', {'fields': ('phone_number', 'username', 'email', 'fullname', 'age')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_superuser', 'last_login', 'groups', 'user_permissions')})
    )

    add_fieldsets = (
        ('Create User', {'fields': ('phone_number', 'email', 'username', 'password1', 'password2')}),
    )

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    readonly_fields = ('last_login',)
    search_fields = ('email', 'fullname')
    ordering = ('fullname',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_readonly_fields(self, request, obj=None):
        print("hello from get_readonly_fields")
        if not request.user.is_superuser:
            return self.readonly_fields + ('is_superuser','is_admin')
        return self.readonly_fields

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    fields = ('code', 'phone')
    list_display = ('code', 'phone', 'created')
    readonly_fields = ('created',)

