import datetime
from datetime import timedelta
from django.utils import timezone
from datetime import date
from .models import *
from Account.models import Technician

myDates = []
def buildMonthlyDays(today):
    f = open("dates.txt", "w")

    for i in range (31):
        print (today)
        myDates.append (today)
        # for each of the day create time slots for that day and for each of the employees and set them to true, we only
        # want this to be triggered once each new day starts.

        # only going to do this once and create time slots for each of the technicians.
        # first what we want to get all of our technicians and iterate over them.
        f.write(str(today)+'\n')
        today = today + datetime.timedelta (days=1)

    f.close()

def buildSchedules(todaysDate):
    # so what we do is we pass in today in order to build the schedules and using our list, if today is not in the list.
    # we remove the first value from the list and we append our new date.
    f = open ("dates.txt", "r")
    for x in f:
        myDates.append (x)
    f.close ( )


    if (str (myDates[0]) == str (todaysDate) + '\n'):
        myDates.clear()
    else:
        # append to list but first remove first value from list and get the next day that should be in our sliding window.
        myDates.pop (0)
        today = date.today()
        from datetime import timedelta
        nextDayInWindow = today + timedelta(days=30)

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
            new_time_slot.save ( )



            # now for each of the new days, what we will do is we modify the time slots based off of the technicians
            # availability that they have set, for an abstract week.
        myDates.clear()


def getTodaysDate(request):
    todaysDate = date.today()
    # buildMonthlyDays(todaysDate)
    buildSchedules (todaysDate)

    return {'todaysDate': todaysDate}
