import datetime


#appointment = Process.close(date=date(2022, 10, 4), appointment_id=4)


#print(Process.close_slots(id=9,date=date(2022, 12, 10)))
#Process.open_slots(date=date(2022, 11, 5))


#print(appointment)
#for i in appointment:
 #   print(i)
 


from timeslot_process import Process
import calendar
from Scheduling.models import TechnicianSchedule, timeSlots
from Account.models import Technician, User
from django.db.models import Q


def main():
    timetable_query = timeSlots.objects.filter(Q(date__gte=datetime.date.today)|Q(date=None)).values()
    count = 0
    for t in timetable_query:
        count += 1
        
    print(count)
    
if __name__ == "__main__":
    main()
    

            

