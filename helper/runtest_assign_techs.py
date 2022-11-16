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
import techs_queue

import calendar


def main():
    sale_list = list(Sale.objects.filter(appointment_id=9)
                            .values("id"))
    sales = Sale.objects.filter(appointment=9).values('id', 'status')
    print(sale_list)
    print(len(sales))

    

if __name__ == "__main__":
    main()

            

