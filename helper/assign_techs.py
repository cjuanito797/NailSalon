import django
import os
import calendar
from datetime import date
import sys

sys.path.append("../NailSalon")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup()
from Scheduling.models import TechnicianSchedule, timeSlots
from Appointments.models import Appointment

def main():
    # get today day
    curr_date = date.today ( )
    dayOfWeek= calendar.day_name[curr_date.weekday ( )]
    # retrieve all available technicians using today day
    available_techs = get_available_techs_on_day(dayOfWeek)

    #--start-test get appointment
    input_id = 3
    test_date = date(2022, 9, 7)
    appointment = Appointment.objects.filter(id=input_id, date=test_date).values_list()
    print(appointment)
    #--end-test get appointment

    # retrieve available technicians' time slot 
    all_time_slots = []
    for tech in available_techs:
        all_time_slots.append(timeSlots.objects.filter(tech=tech, dayOfWeek=dayOfWeek).values_list())
    
    for time_slot in all_time_slots:
        for slot in time_slot:
            print(slot)

def get_available_techs_on_day(dayOfWeek):
    if dayOfWeek == 'Monday':
        return TechnicianSchedule.objects.filter(monday_availability=True).values_list('tech', flat=True)

    elif dayOfWeek == 'Tuesday':
        return TechnicianSchedule.objects.filter(tuesday_availability=True).values_list('tech', flat=True)

    elif dayOfWeek == 'Wednesday':
        return TechnicianSchedule.objects.filter(wednesday_availability=True).values_list('tech', flat=True)

    elif dayOfWeek == 'Thursday':
        return TechnicianSchedule.objects.filter(thursday_availability=True).values_list('tech', flat=True)

    elif dayOfWeek == 'Friday':
        return TechnicianSchedule.objects.filter(friday_availability=True).values_list('tech', flat=True)

    elif dayOfWeek == 'Saturday':
        return TechnicianSchedule.objects.filter(saturday_availability=True).values_list('tech', flat=True)

    else:
        return TechnicianSchedule.objects.filter(sunday_availability=True).values_list('tech', flat=True)

if __name__ == "__main__":
    main()