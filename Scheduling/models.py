from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class TechnicianSchedule (models.Model):
    tech = models.EmailField (_ ('email'), unique=True)

    monday_availability = models.BooleanField (default=False)
    monday_timeIn = models.TimeField ( )
    monday_timeOut = models.TimeField ( )

    # for monday, link a time slot availability model, for this instance
    monday_timeSlots = models.ForeignKey("Scheduling.timeSlots",
                                             related_name="mondayTimeSlots",
                                             on_delete=models.CASCADE,
                                             default=False)


    tuesday_availability = models.BooleanField(default=False)
    tuesday_time_In = models.TimeField()
    tuesday_time_Out = models.TimeField()

    tuesday_timeSlots = models.ForeignKey ("Scheduling.timeSlots",
                                          related_name="tuesdayTimeSlots",
                                          on_delete=models.CASCADE,
                                          default=False)


    wednesday_availability = models.BooleanField (default=False)
    wednesday_time_In = models.TimeField ( )
    wednesday_time_Out = models.TimeField ( )

    wednesday_timeSlots = models.ForeignKey ("Scheduling.timeSlots",
                                           related_name="wednesdayTimeSlots",
                                           on_delete=models.CASCADE,
                                           default=False)

    thursday_availability = models.BooleanField (default=False)
    thursday_time_In = models.TimeField ( )
    thursday_time_Out = models.TimeField ( )

    thursday_timeSlots = models.ForeignKey ("Scheduling.timeSlots",
                                           related_name="thursdayTimeSlots",
                                           on_delete=models.CASCADE,
                                           default=False)

    friday_availability = models.BooleanField (default=False)
    friday_time_In = models.TimeField ( )
    friday_time_Out = models.TimeField ( )

    friday_timeSlots = models.ForeignKey ("Scheduling.timeSlots",
                                           related_name="fridayTimeSlots",
                                           on_delete=models.CASCADE,
                                           default=False)

    saturday_availability = models.BooleanField (default=False)
    saturday_time_In = models.TimeField ( )
    saturday_time_Out = models.TimeField ( )

    saturday_timeSlots = models.ForeignKey ("Scheduling.timeSlots",
                                           related_name="saturdayTimeSlots",
                                           on_delete=models.CASCADE,
                                           default=False)

    sunday_availability = models.BooleanField (default=False)
    sunday_time_In = models.TimeField ( )
    sunday_time_Out = models.TimeField ( )

    sunday_timeSlots = models.ForeignKey ("Scheduling.timeSlots",
                                           related_name="sundayTimeSlots",
                                           on_delete=models.CASCADE,
                                           default=False)

    def __str__(self):
        return self.tech + "\'s schedule"


class timeSlots (models.Model):
    tech = models.EmailField (_ ('email'), unique=False)
    dayOfWeek = models.CharField(blank=False, max_length=9)
    _9_00_am = models.BooleanField (default=False)
    _9_15am = models.BooleanField (default=False)
    _9_30am = models.BooleanField(default=False)
    _9_45am = models.BooleanField(default=False)

    _10_00_am = models.BooleanField (default=False)
    _10_15am = models.BooleanField (default=False)
    _10_30am = models.BooleanField (default=False)
    _10_45am = models.BooleanField (default=False)

    _11_00_am = models.BooleanField (default=False)
    _11_15am = models.BooleanField (default=False)
    _11_30am = models.BooleanField (default=False)
    _11_45am = models.BooleanField (default=False)

    _12_00_pm = models.BooleanField (default=False)
    _12_15am = models.BooleanField (default=False)
    _12_30am = models.BooleanField (default=False)
    _12_45am = models.BooleanField (default=False)

    _1_00_pm = models.BooleanField (default=False)
    _1_15pm = models.BooleanField (default=False)
    _1_30pm = models.BooleanField (default=False)
    _1_45pm = models.BooleanField (default=False)

    _2_00_pm = models.BooleanField (default=False)
    _2_15pm = models.BooleanField (default=False)
    _2_30pm = models.BooleanField (default=False)
    _2_45pm = models.BooleanField (default=False)

    _3_00_pm = models.BooleanField (default=False)
    _3_15pm = models.BooleanField (default=False)
    _3_30pm = models.BooleanField (default=False)
    _3_45pm = models.BooleanField (default=False)

    _4_00_pm = models.BooleanField (default=False)
    _4_15pm = models.BooleanField (default=False)
    _4_30pm = models.BooleanField (default=False)
    _4_45pm = models.BooleanField (default=False)


    def __str__(self):
        return self.tech + "\'s" + " " + self.dayOfWeek + " Availability"
