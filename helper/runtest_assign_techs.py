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
    test = get_time_scheduled_techs(['tuesday', 'thursday', 'saturday'])
        
    print(test)
    

    '''
    timeIn_field_name = "{0}_time_In".format (dayOfWeek.lower())
    timeOut_field_name = "{0}_time_Out".format (dayOfWeek.lower())

    # filter {field_name(provide as custom string): True} (dict)
    time_scheduled_list = list(TechnicianSchedule.objects.filter (
        **{dayOfWeek_field_name: True}
    ).values_list ('tech', timeIn_field_name, timeOut_field_name))
    '''
    
def get_time_scheduled_techs(days_list: list):
    dayOfWeek_fieldname_list = []
    for day in days_list:
        day_fieldname = f"{day}_availability"
        dayOfWeek_fieldname_list.append(day_fieldname)
        
    return dayOfWeek_fieldname_list
    
if __name__ == "__main__":
    main()
    

            

