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
    
        
    return_count = {'scheduled': 0, 'working': 0, 'closed': 0, 'canceled': 0}
    sales = Sale.objects.filter(appointment=2).values('status')
    
    for s in sales:
        if s['status'] == 'scheduled':
            return_count['scheduled'] += 1
        if s['status'] == 'working':
            return_count['working'] += 1
        if s['status'] == 'closed':
            return_count['closed'] += 1
        if s['status'] == 'canceled':
            return_count['canceled'] += 1
            
            
    if (return_count['closed'] + return_count['canceled']) == len(sales):
        print("yes")
        

if __name__ == "__main__":
    main()

            

