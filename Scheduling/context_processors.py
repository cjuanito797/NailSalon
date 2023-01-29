from datetime import timedelta
from datetime import datetime
from django.utils import timezone
from datetime import date
from .models import *
from Account.models import Technician
from Calendar.models import calendarEntry
import calendar
from helper.timeslot_process import Process

myDates = []


# so we want to utilize this function for whenever we are, setting up the website (deployment, new  clone, etc.)  or we
# have just added a new employee.

def buildMonthlyDays(today):
    f = open ("dates.txt", "w")

    for i in range (31):
        print (today)
        myDates.append (today)
        # for each of the day create time slots for that day and for each of the employees and set them to true, we only
        # want this to be triggered once each new day starts.

        # only going to do this once and create time slots for each of the technicians.
        # first what we want to get all of our technicians and iterate over them.
        f.write (str (today) + '\n')

        # build a calendar entry with today's date and add all of the available techs for that day.
        # perhaps we wont delete old time slots as it may helpt with data processing.
        # time slot for each technician on this new day, note that this should only be done once.
        techs = Technician.objects.all ( )

        dayOfWeek = calendar.day_name[today.weekday ( )].lower ( )

        if dayOfWeek == 'Monday':
            techs = Technician.objects.filter (schedule__monday_availability=True)

        elif dayOfWeek == 'Tuesday':
            techs = Technician.objects.filter (schedule__tuesday_availability=True)

        elif dayOfWeek == 'Wednesday':
            techs = Technician.objects.filter (schedule__wednesday_availability=True)

        elif dayOfWeek == 'Thursday':
            techs = Technician.objects.filter (schedule__thursday_availability=True)

        elif dayOfWeek == 'Friday':
            techs = Technician.objects.filter (schedule__friday_availability=True)

        elif dayOfWeek == 'Saturday':
            techs = Technician.objects.filter (schedule__saturday_availability=True)

        else:
            techs = Technician.objects.filter (schedule__sunday_availability=True)

        new_entry = calendarEntry.objects.create (date=today)

        for tech in techs:
            new_entry.technicians.add (tech)

        # so now go ahead and create the calendar entries.
        new_entry.save ( )

        today = today + timedelta (days=1)

    f.close ( )


def buildSchedules(todaysDate):
    # so what we do is we pass in today in order to build the schedules and using our list, if today is not in the list.
    # we remove the first value from the list and we append our new date.

    f = open ("dates.txt", "r")
    for x in f:
        myDates.append (x)
    f.close ( )

    if (str (myDates[0]) == str (todaysDate) + '\n'):
        # nothing to do here.
        myDates.clear ( )
    else:
        # append to list but first remove first value from list and get the next day that should be in our sliding window.

        # delete yesterday's calendar entry.
        # convert myDates[0] (yesterdays date into actual date)
        yesterday = datetime.strptime (myDates[0].strip ('\n'), "%Y-%m-%d").date ( )
        calendarEntry.objects.filter (date=yesterday).delete ( )

        myDates.pop (0)
        today = date.today ( )
        nextDayInWindow = today + timedelta (days=30)

        myDates.append (str (nextDayInWindow) + '\n')

        # so with our new myDates file we can write them to our file.

        f = open ("dates.txt", "w")

        for day in myDates:
            f.write (day)

        f.close ( )

        # perhaps we wont delete old time slots as it may helpt with data processing.
        # time slot for each technician on this new day, note that this should only be done once.
        techs = Technician.objects.all ( )
        for t in techs:
            # add a new time slot for that day
            new_time_slot = timeSlots.objects.create (tech=t.user.email, date=nextDayInWindow)

            # set the hours for the time slot depending on tech and day of the week.

            new_time_slot.save ( )

        Process.open_slots (date=nextDayInWindow)

        # now also each time that we move the window one day to the right, we also need to create a calendar entry with
        # all of the techs working on that day.
        dayOfWeek = calendar.day_name[nextDayInWindow.weekday ( )].lower ( )

        if dayOfWeek == 'Monday':
            techs = Technician.objects.filter (schedule__monday_availability=True)

        elif dayOfWeek == 'Tuesday':
            techs = Technician.objects.filter (schedule__tuesday_availability=True)

        elif dayOfWeek == 'Wednesday':
            techs = Technician.objects.filter (schedule__wednesday_availability=True)

        elif dayOfWeek == 'Thursday':
            techs = Technician.objects.filter (schedule__thursday_availability=True)

        elif dayOfWeek == 'Friday':
            techs = Technician.objects.filter (schedule__friday_availability=True)

        elif dayOfWeek == 'Saturday':
            techs = Technician.objects.filter (schedule__saturday_availability=True)

        else:
            techs = Technician.objects.filter (schedule__sunday_availability=True)

        new_entry = calendarEntry.objects.create (date=nextDayInWindow)

        for tech in techs:
            new_entry.technicians.add (tech)

        # so now go ahead and create the calendar entries.
        new_entry.save ( )

        # now for each of the new days, what we will do is we modify the time slots based off of the technicians
        # availability that they have set, for an abstract week.
        myDates.clear ( )


def getTodaysDate(request):

    todaysDate = date.today ( )
    # buildMonthlyDays(todaysDate)
    buildSchedules (todaysDate)

    return {'todaysDate': todaysDate}
