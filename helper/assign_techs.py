from asyncio.log import logger
import math
from tabnanny import check
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

num_to_word = {1: 'one', 2: 'two', 3: 'three', 4: 'four',
               9: 'nine', 10: 'ten', 11: 'eleven', 
               12: 'twelve',}
num_to_word2 = {13: 'one_', 14: 'two_', 15: 'three_', 16: 'four_',
               9: 'nine_', 10: 'ten_', 11: 'eleven_', 
               12: 'twelve_',}
ERROR_MESSAGE = {1: "Can't find appointment"}

tech_queue = []

def process_queue():
    pass

class Assign_techs:
    def process(appointment_id, check_date):
        try:
            process = _Process(appointment_id, check_date)
            
            # retrieve all available technicians (using today day)
            timeslot_avail_techs = process._get_available_techs()
        
            sale_service = process._split_appointment_to_sales()
            #print(sale_service)
            
            ready_techs = process._sort_tech_by_timeslot(timeslot_avail_techs, sale_service)
            
            #print(sale_service[0]['duration'])
            return sale_service  #--return for test
        except Exception as e:
            logger.error(e)
        
        
class _Process(Assign_techs):
    def __init__(self, appointment_id, check_date):
        self.__appointment_id = appointment_id
        
        #self.current_date = date.today()
        self.current_date = check_date
        
        self.dayOfWeek = calendar.day_name[self.current_date.weekday()]
        self.dayOfWeek_field_name = "{0}_availability".format(
            calendar.day_name[self.current_date.weekday()].lower()
            ) # string concat to match field_name for filter
        
        self.starttime_object = (Appointment.objects.filter(   
                id=appointment_id, date=self.current_date
                ).values_list('start_time', flat=True))[0]
        
        
        #print(self.starttime_object)
        
        
    
    def _get_available_techs(self): 
        # filter {field_name(provide as custom string): True} (dict)
        available_on_day = TechnicianSchedule.objects.filter(
            **{self.dayOfWeek_field_name: True}         
            ).values_list('tech', flat=True)
        
        # retrieve timeslot (dict) for each available technician on current day
        all_time_slots = list((timeSlots.objects.filter(
                tech=tech, date=self.current_date
                ).values()) for tech in available_on_day)
        return all_time_slots
    
    '''  
    def _calculate_timeslot(self,sale_time):
        print(self.starttime_object) #datetime.time
        print(sale_time)               #datetime.timedelta
        print(math.ceil(sale_time.seconds /(60*15)))
        print()
    '''
        
    def _sort_tech_by_timeslot(self, all_time_slots, sale_service):
        
        count = []
        for _ in sale_service:
            count.append(math.ceil(_['duration'].seconds /(60*15)))
        print(count)
        # get slot field_name as start
        hour = self.starttime_object.hour
        minute = self.starttime_object.minute
        #print("hour{0}".format(hour))
        #print("minutes{0}".format(minute))
        
        
        
        minute -= 15
        #print("start slot:")
        #timeslot_field_name = self._convert_time_fieldname(hour,minute)
        #print(timeslot_field_name)
        
        
        for i in count:
            print("move slot:")
            for _ in range(i):
                if minute+15 >= 60:
                    minute = 0
                    hour += 1
                else:
                    minute += 15
                print(self._convert_time_fieldname(hour,minute))
            
        #print(all_time_slots)
        '''
        techs = []
        for time_slot in all_time_slots:
            for slot in time_slot:
                if slot[timeslot_field_name] == True:
                    #techs.append(slot['tech'])
                    print(slot)
        '''
        return None
    
    def _convert_time_fieldname(self, hour, minute):
        hour_string = num_to_word2[hour]
        minute_tostring = ("00_" if minute == 0 else str(minute))
        meridiem = ("am" if hour < 12 else "pm")
        
        return "{0}{1}{2}".format(hour_string, minute_tostring, meridiem)
    
    def _split_appointment_to_sales(self):    
        test_date = self.current_date        #--test input data
        #test_date = self.current_date
        
        # get services' id appointment using appointment_id and date (current date)
        service_ids = Appointment.objects.filter(   
            id=self.__appointment_id, date=test_date    #change date=self.current_date
            ).values_list('services', flat=True)  
        
        # get services' info using services' id list in appointment 
        services = []
        for i in service_ids:
            services.append(
                (Service.objects.filter(id=i).values('id','name', 'price', 'duration'))[0]
                )
        return services



#--main to test assign_techs
def main():
    Assign_techs.process(appointment_id=5, check_date=1)
    
if __name__ == "__main__":
    main()