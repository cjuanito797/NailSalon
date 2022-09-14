from cgitb import lookup
from time import timezone
import django
import os
import calendar
from datetime import date, datetime, timedelta, timezone
import sys

sys.path.append("../NailSalon")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup()

from Scheduling.models import TechnicianSchedule, timeSlots
from Appointments.models import Appointment, Service

class Assign_techs:
    def __init__(self):
        self.current_date = date.today()
        #print((self.current_date - timedelta(1)))
        self.dayOfWeek = calendar.day_name[self.current_date.weekday()]
        self.dayOfWeek_field_name = "{0}_availability".format(
            calendar.day_name[self.current_date.weekday()].lower()
            )
        
    '''
    def _get_available_techs_on_day(self):
        if self.dayOfWeek == 'Monday':
            return TechnicianSchedule.objects.filter(monday_availability=True).values_list('tech', flat=True)

        elif self.dayOfWeek == 'Tuesday':
            return TechnicianSchedule.objects.filter(tuesday_availability=True).values_list('tech', flat=True)

        elif self.dayOfWeek == 'Wednesday':
            return TechnicianSchedule.objects.filter(wednesday_availability=True).values_list('tech', flat=True)

        elif self.dayOfWeek == 'Thursday':
            return TechnicianSchedule.objects.filter(thursday_availability=True).values_list('tech', flat=True)

        elif self.dayOfWeek == 'Friday':
            return TechnicianSchedule.objects.filter(friday_availability=True).values_list('tech', flat=True)

        elif self.dayOfWeek == 'Saturday':
            return TechnicianSchedule.objects.filter(saturday_availability=True).values_list('tech', flat=True)

        else:
            return TechnicianSchedule.objects.filter(sunday_availability=True).values_list('tech', flat=True)
    '''

    def _get_available_techs_on_day(self): 
        available_on_day = TechnicianSchedule.objects.filter(
            **{self.dayOfWeek_field_name: True}
            ).values_list('tech', flat=True)
        
        # retrieve time slot for each available technician on current day
        all_time_slots = list((timeSlots.objects.filter(
                tech=tech, dayOfWeek=self.dayOfWeek
                ).values_list()) for tech in available_on_day)
        '''
        for tech in available_on_day:
            all_time_slots.append(timeSlots.objects.filter(
                tech=tech, dayOfWeek=self.dayOfWeek
                ).values_list())
        '''

        for time_slot in all_time_slots:
            for slot in time_slot:
                print(slot)
    
    def _get_available_techs_on_time(self):
        pass
    
    def _split_appointment_to_sales(self, appointment_id):
        test_date = date(2022, 9, 14)     #--test input data
        
        # get services' id appointment using appointment_id and date (current date)
        appointment = Appointment.objects.filter(   #change date=self.current_date
            id=appointment_id, date=test_date
            ).values_list('services', flat=True)  
        
        # get services' info using services' id list in appointment 
        services = []
        for i in appointment:
            services.append(
                list(Service.objects.filter(id=i).values_list('id', 'price', 'duration'))
                )
        return services
    
def process_appointment_id(appointment_id):
    process = Assign_techs()
    
    # retrieve all available technicians using today day
    available_techs = process._get_available_techs_on_day()
    #print(available_techs)
    
    
            
    appointment = process._split_appointment_to_sales(appointment_id)
    return appointment  #--return for test


#--main to test assign_techs
def main():
    process_appointment_id(3)
    
if __name__ == "__main__":
    main()
    



