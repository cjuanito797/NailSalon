from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class weeklySchedule (models.Model):
    tech = models.EmailField (_ ('email'), unique=True)

    monday_availability = models.BooleanField (default=False)
    monday_timeIn = models.TimeField ( )
    monday_timeOut = models.TimeField ( )

    # for monday, link a time slot availability model, for this instance
    monday_timeSlots = models.OneToOneField ("Scheduling.timeSlots",
                                             related_name="mondayTimeSlots",
                                             on_delete=models.CASCADE,
                                             default=False)


    tuesday_availability = models.BooleanField(default=False)



class timeSlots (models.Model):
    tech = models.EmailField (_ ('email'), unique=True)
    dayOfWeek = models.CharField(blank=False, max_length=9)
    _9_00_am = models.BooleanField (default=False)
    _9_15am = models.BooleanField (default=False)
