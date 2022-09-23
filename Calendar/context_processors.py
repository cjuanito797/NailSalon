from .models import calendarEntry
from datetime import datetime
import calendar
from Account.models import Technician

# do this only once, for every date in our dates calendar read them into an array.
myDates = []


def buildEntries():
    # read from dates.txt
    file = open ("dates.txt", "r")

    # read the data into our myDates list and strip the newline.
    for x in file:
        myDates.append (x.strip ('\n'))

    file.close ( )

    # now for each of these entries,build a calendar entry with the technician that is available for that day, so for this t
    # toy program what we want to do is for each day get the corresponding weekday, i.e. Sunday, Saturday, Etc.
    # so first we should try to and do is to format the string to an actual datetime.
    for d in myDates:

        curr_date = datetime.strptime (d, "%Y-%m-%d").date ( )

        # now get the day of the week and print it alongside the date.
        dayOfWeek = calendar.day_name[curr_date.weekday ( )].lower ( )

        print (curr_date, dayOfWeek)
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

        new_entry = calendarEntry.objects.create (date=curr_date)

        for tech in techs:
            new_entry.technicians.add(tech)
            print ("\t" + tech.user.email)

        # so now go ahead and create the calendar entries.
        new_entry.save ( )

    myDates.clear ( )


def buildCalendar(request):
    return {"None": None}
