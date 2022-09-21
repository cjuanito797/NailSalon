import datetime
import pickle

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
        f.write(str(today))
        today = today + datetime.timedelta (days=1)

    f.close()



def buildSchedules(today):
    # so what we do is we pass in today in order to build the schedules and using our list, if today is not in the list.
    # we remove the first value from the list and we append our new date.
    if today in myDates:
        pass
    else:
        # append to list but first remove first value from list.
        myDates.pop (0)
        myDates.append (today)

        # perhaps we wont delete old time slots as it may helpt with data processing.
        # time slot for each technician on this new day, note that this should only be done once.
        techs = Technician.objects.all()
        for t in techs:
            # add a new time slot for that day
            new_time_slot = timeSlots.objects.create(tech=t.user.email,date=today)
            new_time_slot.save()
        print ("Inside build schedules!")

def getTodaysDate(request):
    today = date.today ( )
    buildMonthlyDays (today)
    buildSchedules (today)

    return {'today': today}
