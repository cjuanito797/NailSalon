import datetime
import json
import math
from timeslot_process import Process
import datetime


#appointment = Process.close(date=date(2022, 10, 4), appointment_id=4)


#print(Process.close_slots(id=9,date=date(2022, 12, 10)))
#Process.open_slots(date=date(2022, 11, 5))


#print(appointment)
#for i in appointment:
 #   print(i)
 
 
 
from Appointments.models import Appointment, Sale, Service
from Account.models import Technician, User
from Scheduling.models import TechnicianSchedule, timeSlots
import techs_queue, timeslot_process

import calendar
from django.core import serializers


def main():
    
        
    timetable_query = timeSlots.objects.all().values()
    fieldname_list = timeslot_process.collect_time_fieldname (9, 0, [32])
    
    
    timetable_date_list = []
    for timeslot in timetable_query:
        
        if timeslot['date'] not in timetable_date_list:
            timetable_date_list.append(timeslot['date'])
        
        count = 0
        for field in fieldname_list:
            timeslot[count] = timeslot.pop(field)
            count += 1
        timeslot['date'] = str(timeslot['date'])
        timeslot['tech'] = list(User.objects.filter(email=timeslot['tech']).values("first_name", "last_name"))[0]
        del timeslot['id']
        del timeslot['arrive_time']
        
    print(timetable_date_list)
    print(timetable_query[0])

if __name__ == "__main__":
    main()

            

