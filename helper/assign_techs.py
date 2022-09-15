import django
import os
import calendar
from datetime import date, datetime, timedelta
import sys

sys.path.append("../NailSalon")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup()

from Scheduling.models import TechnicianSchedule, timeSlots
from Appointments.models import Appointment, Service

class Assign_techs:
    def process(appointment_id):
        process = _Process(appointment_id)
        
        # retrieve all available technicians using today day
        print(process._get_available_techs())
        
        sale_service = process._split_appointment_to_sales()
        return sale_service  #--return for test


class _Process(Assign_techs):
    def __init__(self, appointment_id):
        self.__appointment_id = appointment_id
        self.current_date = date.today()
        self.dayOfWeek = calendar.day_name[self.current_date.weekday()]
        self.dayOfWeek_field_name = "{0}_availability".format(
            calendar.day_name[self.current_date.weekday()].lower()
            ) # string concat to match field_name for filter
        
    
    def _setup_timeslot_dict():
        pass
    
    '''
    def __get_available_techs_on_day(self):
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
    def _get_available_techs(self): 
        # filter {field_name(provide as custom string): True} (dict)
        available_on_day = TechnicianSchedule.objects.filter(
            **{self.dayOfWeek_field_name: True}         
            ).values_list('tech', flat=True)
        
        # retrieve timeslot (dict) for each available technician on current day
        all_time_slots = list((timeSlots.objects.filter(
                tech=tech, dayOfWeek=self.dayOfWeek
                ).values()) for tech in available_on_day)
        return self.__sort_tech_by_timeslot(all_time_slots)
        '''
        for tech in available_on_day:
            all_time_slots.append(timeSlots.objects.filter(
                tech=tech, dayOfWeek=self.dayOfWeek
                ).values_list())
        '''
        
    def __sort_tech_by_timeslot(self, all_time_slots):
        techs = []
        for time_slot in all_time_slots:
            for slot in time_slot:
                #print(slot)
                if slot['nine_15am'] == True:
                    techs.append(slot['tech'])
        return techs
    
    def _split_appointment_to_sales(self):
        #test_date = date(2022, 9, 14)     #--test input data
        test_date = date(2022, 9, 7)
        
        # get services' id appointment using appointment_id and date (current date)
        appointments = Appointment.objects.filter(   #change date=self.current_date
            id=self.__appointment_id, date=test_date
            ).values_list('services', flat=True)  
        
        # get services' info using services' id list in appointment 
        services = []
        for i in appointments:
            services.append(
                list(Service.objects.filter(id=i).values_list('id','name', 'price', 'duration'))
                )
        return services



#--main to test assign_techs
def main():
    Assign_techs.process(appointment_id=3)
    
if __name__ == "__main__":
    main()
    



