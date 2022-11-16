from django.contrib import admin
from .models import Service, Appointment, Category, Sale

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
    list_display = ['customer', 'technician', 'start_time', 'end_time', 'date', 'details', 'image']

    list_display = ['customer', 'technician', 'start_time', 'end_time', 'date', 'details', 'image']

    list_display = ['customer', 'technician', 'start_time', 'end_time', 'date', 'details', 'image']
    
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['service', 'technician', 'appointment', 'status']
    