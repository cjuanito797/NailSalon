from django.contrib import admin
from .models import TechnicianSchedule, timeSlots
# Register your models here.

@admin.register(TechnicianSchedule)
class scheduleAdmin (admin.ModelAdmin):
    list_display = ['tech']

@admin.register (timeSlots)
class timeSlotsAdmin (admin.ModelAdmin):
    list_display = ['tech']
