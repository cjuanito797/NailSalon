import datetime
import json
from timeslot_process import Process


#appointment = Process.close(date=date(2022, 10, 4), appointment_id=4)


#print(Process.close_slots(id=7,date=date(2022, 10, 12)))
#Process.open_slots(date=date(2022, 11, 5))


#print(appointment)
#for i in appointment:
 #   print(i)
 
 
 
from Appointments.models import Appointment, Sale, Service
from Account.models import Technician, User
from Scheduling.models import TechnicianSchedule
from datetime import date
import calendar


all_email = (User.objects.all().values_list("email"))
for i in all_email:
    print(i[0])



