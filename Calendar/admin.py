from django.contrib import admin
from .models import calendarEntry


# Register your models here.
@admin.register(calendarEntry)
class calendarEntry(admin.ModelAdmin):
    list_display = ['date']