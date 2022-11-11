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

appointment_query = Appointment.objects.all().values(
        'id', 
        'customer', 
        'start_time', 
        'end_time', 
        'totalCharge',
        'date'
        )
appointment_list = []
apt_date_list = []
for a in appointment_query:
    a['customer'] = list(User.objects.filter(id=a['customer']).values("first_name", "last_name"))[0]
    appointment_list.append(a)
    if a['date'] not in apt_date_list:
        apt_date_list.append(a['date'])
    

            

