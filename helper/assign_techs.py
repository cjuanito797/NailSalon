from asyncio.log import logger
import math
import django
import os
import calendar
import sys

sys.path.append ("../NailSalon")
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup ( )

from Scheduling.models import TechnicianSchedule, timeSlots
from Appointments.models import Appointment, Service, Sale
from Account.models import Technician, User

num_to_word = {13: 'one_', 14: 'two_', 15: 'three_', 16: 'four_',
               9: 'nine_', 10: 'ten_', 11: 'eleven_',
               12: 'twelve_', }
ERROR_MESSAGE = {0: "Cannot find appointment", 1: "Cannot find open timeslot for services"}

tech_queue = []

def process_queue():
    pass

class Process:
    def processing(**kargs):
        if len(kargs) == 2:      # Process appointment (by appointment_id, date)
            __appointment_id = kargs['appointment_id']
            check_date = kargs['date']
            try:
                process = _Process(check_date, __appointment_id)
                # retrieve all available technicians (using today day)
                timeslot_avail_techs = process._get_available_techs ( )
                # split appointment to sales
                sale_service = process._split_appointment_to_sales ( )
                # find and assign open technician for sales
                assign_tech = process._sort_and_assign_tech (timeslot_avail_techs, sale_service)
                # retrieve technician name for return
                tech_name = User.objects.filter (email=assign_tech).values_list ('first_name', 'last_name')[0]
                # set return value (tech first, last name)
                return f"{tech_name[0]} {tech_name[1]}" # --return for test
            except IndexError as ie:
                logger.error (ie)
        elif len(kargs) == 1:    # Initialize timeslot for new day (by date)
            date = kargs['date']
            process = _Process(date)
            timeslot_avail_techs = process._get_available_techs ( )
            
            # total timeslot in one day
            count = 32
            # get slot field_name as start
            hour = 9
            minute = 0
            minute -= 15    # subtract 15 so the next slot will be 9:00

            # Prepare all timeslot fieldname depend for total duration of all services
            fieldname_list = []
            for _ in range(count):
                if minute + 15 >= 60:
                    minute = 0
                    hour += 1
                else:
                    minute += 15
                fieldname_list.append(_convert_time_fieldname(hour, minute))

            for timeslot in timeslot_avail_techs:
                for field in fieldname_list:
                    assign = timeSlots.objects.get (tech=timeslot['tech'], date=date)
                    setattr (assign, field, True)
                    assign.save ( )

class _Process:
    def __init__(self, check_date, appointment_id=None):
        # self.current_date = date.today()
        self.current_date = check_date

        self.dayOfWeek = calendar.day_name[self.current_date.weekday ( )]
        self.dayOfWeek_field_name = "{0}_availability".format (
            calendar.day_name[self.current_date.weekday ( )].lower ( )
        )  # string concat to match field_name for filter

        if appointment_id is not None:
            try:
                self.__appointment_id = appointment_id
                self.starttime_object = (Appointment.objects.filter (
                    id=appointment_id, date=self.current_date
                ).values_list ('start_time', flat=True))[0]
            except IndexError:
                raise IndexError ("appointment error")

    def _get_available_techs(self):
        # filter {field_name(provide as custom string): True} (dict)
        available_on_day = TechnicianSchedule.objects.filter (
            **{self.dayOfWeek_field_name: True}
        ).values_list ('tech', flat=True)

        # retrieve timeslot (dict) for each available technician on current day
        all_time_slots = list ((timeSlots.objects.filter (
            tech=tech, date=self.current_date
        ).values ( )[0]) for tech in available_on_day)
        return all_time_slots

    def _sort_and_assign_tech(self, all_time_slots, sale_service):
        # count number of timefield for each service
        count = []
        for _ in sale_service:
            count.append (math.ceil (_['duration'].seconds / (60 * 15)))

        # get slot field_name as start
        hour = self.starttime_object.hour
        minute = self.starttime_object.minute

        minute -= 15

        # Prepare all timeslot fieldname depend for total duration of all services
        fieldname_list = []
        for i in count:
            # print("move slot:")
            for _ in range (i):
                if minute + 15 >= 60:
                    minute = 0
                    hour += 1
                else:
                    minute += 15
                fieldname_list.append (_convert_time_fieldname (hour, minute))

        #print(sale_service)
        #print(count)
        #print(fieldname_list)
        #print(all_time_slots)
        # Find technician who open to do all services in appointment
        tech_email = None
        for tech in all_time_slots:
            count = 0
            for field in fieldname_list:
                count += (1 if tech[field] == True else 0)
            if count == len (fieldname_list):
                tech_email = tech['tech']
            break
        
        # Set time slot and tech into sales
        if tech_email != None:
            # Create new Sales
            for s in sale_service:
                Sale.objects.create(
                    service=Service.objects.get(id=s['id']),
                    technician=User.objects.get(email=tech_email),
                    appointment=Appointment.objects.get(id=self.__appointment_id),
                )
            # Set time slot to False (busy) for open technician
            for field in fieldname_list:
                assign = timeSlots.objects.get (tech=tech_email, date=self.current_date) # ****
                setattr (assign, field, False)
                assign.save ( )

        else:
            tech_email == -1

        return tech_email

    def _split_appointment_to_sales(self):
        test_date = self.current_date  # --test input data
        # test_date = self.current_date

        # get services' id appointment using appointment_id and date (current date)
        service_ids = Appointment.objects.filter (
            id=self.__appointment_id, date=test_date  # change date=self.current_date
        ).values_list ('services', flat=True)

        # get services' info using services' id list in appointment 
        services = []
        for i in service_ids:
            services.append (
                (Service.objects.filter (id=i).values ('id', 'name', 'price', 'duration'))[0]
            )
        return services

def _convert_time_fieldname(hour, minute):
    hour_string = num_to_word[hour]
    minute_tostring = ("00_" if minute == 0 else str (minute))
    meridiem = ("am" if hour < 12 else "pm")
    return "{0}{1}{2}".format (hour_string, minute_tostring, meridiem)

