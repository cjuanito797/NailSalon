from django.contrib import admin
from .models import weeklySchedule, timeSlots
# Register your models here.

@admin.register(weeklySchedule)
class weeklyScheduleAdmin (admin.ModelAdmin):
    list_display = ['tech']

@admin.register (timeSlots)
class timeSlotsAdmin (admin.ModelAdmin):
    list_display = ['tech']
