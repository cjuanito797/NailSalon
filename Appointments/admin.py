from django.contrib import admin
from .models import Service, Appointment, Category

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name','price', 'duration', 'category']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Appointment)
class AppointmentModel(admin.ModelAdmin):
    list_display = ['customer', 'start_time', 'end_time', 'date']