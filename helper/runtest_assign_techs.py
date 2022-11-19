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


def main():
    
        
    # build fresh queue for test
    #techs_queue.build_fresh_wait_queue(datetime.date(2022, 12, 11))
    
    all_timeslot = list(timeSlots.objects.filter(date=datetime.date(2022,12,11)).values())
    #print(a[0])
    fieldname_list = timeslot_process.collect_time_fieldname (10, 30, [4])
    for timeslot in all_timeslot:
        count = 0
        for field in fieldname_list:
            timeslot[count] = timeslot.pop(field)
            count += 1
        del timeslot['id']
        del timeslot['arrive_time']
        print(timeslot)
    
    

if __name__ == "__main__":
    main()

            

