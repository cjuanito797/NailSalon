from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
import calendar


# Create your models here.

class TechnicianSchedule (models.Model):
    tech = models.EmailField (_ ('email'), unique=True)

    monday_availability = models.BooleanField (default=False)
    monday_timeIn = models.TimeField ( )
    monday_timeOut = models.TimeField ( )

    tuesday_availability = models.BooleanField (default=False)
    tuesday_time_In = models.TimeField ( )
    tuesday_time_Out = models.TimeField ( )


    wednesday_availability = models.BooleanField (default=False)
    wednesday_time_In = models.TimeField ( )
    wednesday_time_Out = models.TimeField ( )



    thursday_availability = models.BooleanField (default=False)
    thursday_time_In = models.TimeField ( )
    thursday_time_Out = models.TimeField ( )



    friday_availability = models.BooleanField (default=False)
    friday_time_In = models.TimeField ( )
    friday_time_Out = models.TimeField ( )



    saturday_availability = models.BooleanField (default=False)
    saturday_time_In = models.TimeField ( )
    saturday_time_Out = models.TimeField ( )



    sunday_availability = models.BooleanField (default=False)
    sunday_time_In = models.TimeField ( )
    sunday_time_Out = models.TimeField ( )



    def __str__(self):
        return self.tech + "\'s schedule"

    # get current days time slots, so determine which time slots we want to return for displaying of schedules.
    def getTodaysTimeSlots(self):
        # return the correct time slots dependent on the day of the week.
        curr_date = date.today ( )
        dayOfWeek = calendar.day_name[curr_date.weekday ( )].lower ( )
        print (dayOfWeek)
        if dayOfWeek == 'Monday':
            return self.monday_timeSlots

        elif dayOfWeek == 'Tuesday':
            return self.tuesday_timeSlots

        elif dayOfWeek == 'Wednesday':
            return self.wednesday_timeSlots

        elif dayOfWeek == 'Thursday':
            return self.thursday_timeSlots

        elif dayOfWeek == 'Friday':
            return self.friday_timeSlots

        elif dayOfWeek == 'Saturday':
            return self.saturday_timeSlots

        else:
            return self.sunday_timeSlots


class timeSlots (models.Model):
    tech = models.EmailField (_ ('email'), unique=False)
    date = models.DateField (blank=True)
    nine_00_am = models.BooleanField (default=False)
    nine_15am = models.BooleanField (default=False)
    nine_30am = models.BooleanField (default=False)
    nine_45am = models.BooleanField (default=False)

    ten_00_am = models.BooleanField (default=False)
    ten_15am = models.BooleanField (default=False)
    ten_30am = models.BooleanField (default=False)
    ten_45am = models.BooleanField (default=False)

    eleven_00_am = models.BooleanField (default=False)
    eleven_15am = models.BooleanField (default=False)
    eleven_30am = models.BooleanField (default=False)
    eleven_45am = models.BooleanField (default=False)

    twelve_00_pm = models.BooleanField (default=False)
    twelve_15pm = models.BooleanField (default=False)
    twelve_30pm = models.BooleanField (default=False)
    twelve_45pm = models.BooleanField (default=False)

    one_00_pm = models.BooleanField (default=False)
    one_15pm = models.BooleanField (default=False)
    one_30pm = models.BooleanField (default=False)
    one_45pm = models.BooleanField (default=False)

    two_00_pm = models.BooleanField (default=False)
    two_15pm = models.BooleanField (default=False)
    two_30pm = models.BooleanField (default=False)
    two_45pm = models.BooleanField (default=False)

    three_00_pm = models.BooleanField (default=False)
    three_15pm = models.BooleanField (default=False)
    three_30pm = models.BooleanField (default=False)
    three_45pm = models.BooleanField (default=False)

    four_00_pm = models.BooleanField (default=False)
    four_15pm = models.BooleanField (default=False)
    four_30pm = models.BooleanField (default=False)
    four_45pm = models.BooleanField (default=False)

    def __str__(self):
        return self.tech + "\'s" + " " + str (self.date) + " Availability"
