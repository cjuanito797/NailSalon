import datetime
import json
from timeslot_process import Process
from datetime import date


#appointment = Process.close(date=date(2022, 10, 4), appointment_id=4)


#print(Process.close_slots(id=9,date=date(2022, 12, 10)))
#Process.open_slots(date=date(2022, 11, 5))


#print(appointment)
#for i in appointment:
 #   print(i)
 
 
 
from Appointments.models import Appointment, Sale, Service
from Account.models import Technician, User
from Scheduling.models import TechnicianSchedule

import calendar

tech_query = list(Technician.objects.all().values('id', 'user'))
for t in tech_query:
    print(t['user'])
