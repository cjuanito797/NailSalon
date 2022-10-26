from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
import calendar


# Create your models here.

class TechnicianSchedule (models.Model):
    tech = models.EmailField (_ ('email'), unique=True)

    monday_availability = models.BooleanField (default=False)
    monday_time_In = models.TimeField (blank=True)
    monday_time_Out = models.TimeField (blank=True)

    tuesday_availability = models.BooleanField (default=False)
    tuesday_time_In = models.TimeField (blank=True)
    tuesday_time_Out = models.TimeField (blank=True)

    wednesday_availability = models.BooleanField (default=False)
    wednesday_time_In = models.TimeField (blank=True)
    wednesday_time_Out = models.TimeField (blank=True)

    thursday_availability = models.BooleanField (default=False)
    thursday_time_In = models.TimeField (blank=True)
    thursday_time_Out = models.TimeField (blank=True)

    friday_availability = models.BooleanField (default=False)
    friday_time_In = models.TimeField (blank=True)
    friday_time_Out = models.TimeField (blank=True)

    saturday_availability = models.BooleanField (default=False)
    saturday_time_In = models.TimeField (blank=True)
    saturday_time_Out = models.TimeField (blank=True)

    sunday_availability = models.BooleanField (default=False)
    sunday_time_In = models.TimeField (blank=True)
    sunday_time_Out = models.TimeField (blank=True)

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
    arrive_time = models.TimeField (blank=True, null=True)

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
        return self.tech + "\'s" + " " + str (self.date)

    def list(self):
        timeSlotsList = [self.nine_00_am, self.nine_15am, self.nine_30am, self.nine_45am,
                         self.ten_00_am, self.ten_15am, self.ten_30am, self.ten_45am,
                         self.eleven_00_am, self.eleven_15am, self.eleven_30am, self.eleven_45am,
                         self.twelve_00_pm, self.twelve_15pm, self.twelve_30pm, self.twelve_45pm,
                         self.one_00_pm, self.one_15pm, self.one_30pm, self.one_45pm,
                         self.two_00_pm, self.two_15pm, self.two_30pm, self.two_45pm,
                         self.three_00_pm, self.three_15pm, self.three_30pm, self.three_45pm,
                         self.four_00_pm, self.four_15pm, self.four_30pm, self.four_45pm]
        return timeSlotsList

    def timeDictionary(self):
        times = {
            '9:00am': self.nine_00_am,
            '9:15am': self.nine_15am,
            '9:30am': self.nine_30am,
            '9:45am': self.nine_45am,
            '10:00am': self.ten_00_am,
            '10:15am': self.ten_15am,
            '10:30am': self.ten_30am,
            '10:45am': self.ten_45am,
            '11:00am': self.eleven_00_am,
            '11:15am': self.eleven_15am,
            '11:30am': self.eleven_30am,
            '11:45am': self.eleven_45am,
            '12:00pm': self.twelve_00_pm,
            '12:15pm': self.twelve_15pm,
            '12:30pm': self.twelve_30pm,
            '12:45pm': self.twelve_45pm,
            '1:00pm': self.one_00_pm,
            '1:15pm': self.one_15pm,
            '1:30pm': self.one_30pm,
            '1:45pm': self.one_45pm,
            '2:00pm': self.two_00_pm,
            '2:15pm': self.two_15pm,
            '2:30pm': self.two_30pm,
            '2:45pm': self.two_45pm,
            '3:00pm': self.three_00_pm,
            '3:15pm': self.three_15pm,
            '3:30pm': self.three_30pm,
            '3:45pm': self.three_45pm,
            '4:00pm': self.four_00_pm,
            '4:15pm': self.four_15pm,
            '4:30pm': self.four_30pm,
            '4:45pm': self.four_45pm
        }

        return times
