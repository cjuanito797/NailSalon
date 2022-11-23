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
from Account.models import Technician


def main():
    
    process = Process.open_slots(tech_id=1, 
                                 duration=datetime.timedelta(seconds=1800), 
                                 starttime=datetime.time(9,45),
                                 date=datetime.date(2022, 12, 1))
    
    
if __name__ == "__main__":
    main()
    

            

