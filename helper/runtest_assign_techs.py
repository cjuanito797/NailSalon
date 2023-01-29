
import django
import os
import sys
import math

sys.path.append ("../NailSalon")
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup ( )


#appointment = Process.close(date=date(2022, 10, 4), appointment_id=4)


#print(Process.close_slots(id=9,date=date(2022, 12, 10)))
#Process.open_slots(date=date(2022, 11, 5))


#print(appointment)
#for i in appointment:
 #   print(i)
 

import math

from timeslot_process import Process
import calendar
from Scheduling.models import TechnicianSchedule, timeSlots
from Account.models import Technician, User
from django.db.models import Q
from Appointments.models import Appointment, Service
import helper.appointment_queue as appointment_queue


import datetime

def main():
    next = datetime.time(9,17,0)
    print(datetime.datetime.now().time())
    
    next_slot = math.floor((next.minute + 15)/15)
    
    
    
    if next_slot > 4:
        next = datetime.time(next.hour + 1, 0, 0)
    else:
        next = datetime.time(next.hour, next_slot * 15, 0)
    print(next)
        
    
    

if __name__ == "__main__":
    main()
    

            

