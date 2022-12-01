
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
    cart = ["Acrylic Fill In", "Acrylic Full Set",]
    
    #service_list = []
    
    new_appointment = Appointment.objects.create (
                customer_id=1,
                technician_id=None,

                # iterate through the cart and add the services
                # currently there is no way to add the quantity, we could create a ServiceOrderItem

                start_time=datetime.time (10, 30, 00),
                end_time=datetime.time (11, 30, 00),
                totalDuration=60,
                date=datetime.date.today(),
                totalCharge=50
            )
    for item in cart:
        new_appointment.services.add(Service.objects.filter (name__exact=item).get ( ))
    new_appointment.save()
    
    print(new_appointment.technician)
    '''
    if new_appointment.id is None:
        print("None")
    else:
        print("not None")
    '''
        
    
    

if __name__ == "__main__":
    main()
    

            

