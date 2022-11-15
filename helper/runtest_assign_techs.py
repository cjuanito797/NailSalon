import datetime
import json
from timeslot_process import Process
from datetime import date, timedelta, datetime


#appointment = Process.close(date=date(2022, 10, 4), appointment_id=4)


#print(Process.close_slots(id=9,date=date(2022, 12, 10)))
#Process.open_slots(date=date(2022, 11, 5))


#print(appointment)
#for i in appointment:
 #   print(i)
 
 
 
from Appointments.models import Appointment, Sale, Service
from Account.models import Technician, User
from Scheduling.models import TechnicianSchedule, timeSlots

import calendar


def main():
    build_fresh_wait_queue(date(2022,12,11))


def build_fresh_wait_queue(today_date: date): # change to queue of all tech of the day()
    timeslots = []
    #test = []
    temp = list(timeSlots.objects.filter(date=today_date).values('tech', 'arrive_time'))
    for t in temp:
        if t['arrive_time'] != None:
            t['arrive_time'] = a = datetime.combine(date.min, t['arrive_time']) - datetime.min
            timeslots.append(t)
        
    lines = "_WAIT:\n"
    sorted_list = sorted(timeslots, key=lambda x: x['arrive_time'])
    for sl in sorted_list:
        lines += f"{sl['tech']}:0\n"
    lines += "_WORD:\n"
    print(lines)
            
    

    

if __name__ == "__main__":
    main()

            

