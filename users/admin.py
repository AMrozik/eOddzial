from django.contrib import admin
from .models import Account
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Account
    list_display = ('email', 'first_name', 'last_name', 'medic', 'is_ordynator', 'is_medic', 'is_secretary', 'is_planist', 'is_superuser', 'is_admin')

    list_filter = ('email', 'first_name', 'last_name', 'medic', 'is_ordynator', 'is_medic', 'is_secretary', 'is_planist', 'is_superuser', 'is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'medic', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_ordynator', 'is_medic', 'is_secretary', 'is_planist', 'is_superuser', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'medic', 'password1', 'password2', 'is_ordynator', 'is_medic', 'is_secretary', 'is_planist')}
        ),
    )
    search_fields = ('email', 'last_name', 'first_name')
    ordering = ('email',)


admin.site.register(Account, CustomUserAdmin)
