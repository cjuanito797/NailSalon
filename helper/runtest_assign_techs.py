import datetime
import json
from timeslot_process import Process


#appointment = Process.close(date=date(2022, 10, 4), appointment_id=4)


#print(Process.close_slots(id=7,date=date(2022, 10, 12)))
#Process.open_slots(date=date(2022, 11, 5))


#print(appointment)
#for i in appointment:
 #   print(i)
 
 
 
from Appointments.models import Appointment, Sale, Service
from Account.models import Technician, User
from Scheduling.models import TechnicianSchedule
from datetime import date
import calendar


check_date = date.today()
current_date = check_date
dayOfWeek = calendar.day_name[current_date.weekday ( )]
dayOfWeek_field_name = "{0}_availability".format (
    calendar.day_name[current_date.weekday ( )].lower ( )
)  # string concat to match field_name for filter

timeIn_field_name = "{0}_time_In".format (dayOfWeek.lower())
timeOut_field_name = "{0}_time_Out".format (dayOfWeek.lower())

# filter {field_name(provide as custom string): True} (dict)
scheduled_tech = list(TechnicianSchedule.objects.filter (
    **{dayOfWeek_field_name: True}
).values_list ('tech'))

scheduled_techlist = []
for t_email in scheduled_tech:
    t_list = {'email':'', 'name':{}}
    t_list['name'] = list(User.objects.filter(
            email=t_email[0]).values(
                'first_name','last_name'))[0]
    t_list['email'] = t_email[0]
    scheduled_techlist.append(t_list)

scheduled_techlist = json.dumps(scheduled_techlist)
print(scheduled_techlist)
'''
scheduled_tech:
[{
    email,
    name: {first_name,last_name},
}]

'''

#print(dayOfWeek_field_name)
#print(scheduled_tech)




