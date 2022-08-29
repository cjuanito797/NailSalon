from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User, Technician, Customer
from .forms import RegistrationForm


class CustomUserAdmin (UserAdmin):
    add_form = RegistrationForm
    list_display = ('email', 'first_name', 'last_name')
    list_filter = ('email', 'is_staff', 'isTechnician')
    search_fields = ('email')

    fieldsets = (
        (
            'Fields', {
                'fields': ('email', 'first_name', 'last_name', 'street_num', 'city', 'state', 'zipcode', 'isTechnician')
            },
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register (User, CustomUserAdmin)


@admin.register (Technician)
class TechAdmin (admin.ModelAdmin):
    list_display = ['user']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user']

