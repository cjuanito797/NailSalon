import logging
import traceback
import math
import django
import os
import calendar
from datetime import datetime
import sys

sys.path.append ("../NailSalon")
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup ( )

from Scheduling.models import TechnicianSchedule, timeSlots
from Appointments.models import Appointment, Service, Sale
from Account.models import Technician, User

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

num_to_word = {13: 'one_', 14: 'two_', 15: 'three_', 16: 'four_',
               9: 'nine_', 10: 'ten_', 11: 'eleven_',
               12: 'twelve_', }
ERROR_MESSAGE = {0: "Cannot find appointment", 1: "Cannot find open timeslot for services"}

class Process:
    def close_slots(**kargs):
        if len(kargs) == 2:      # close timeslot by appointment (by id(appointment), date)
            appointment_id = kargs['id']
            sale_count = Sale.objects.filter(appointment=appointment_id).count()
            if sale_count > 0:
                return "Appoinment is already triggered!"
            check_date = kargs['date']
            
            process = _Process(check_date, appointment_id)
            # split appointment to sales
            sale_service = process._split_appointment_to_sales ( )
            # retrieve all available technicians (using today day)
            avail_techs_timeslots = process._get_techs_timeslots ( )
            # find and assign open technician for sales
            print(avail_techs_timeslots)
            assign_tech = process._assign_chosen_tech (avail_techs_timeslots['tech'], sale_service)
            # retrieve technician name for return
            tech_name = User.objects.filter (email=assign_tech).values_list ('first_name', 'last_name')[0]
            # set return value (tech first, last name)
            return f"{tech_name[0]} {tech_name[1]}" # --return for test
        
        elif len(kargs) == 1:       # move sale status by appointment (by id(appointment))  
            appointment_id = kargs['id']
            sales = Sale.objects.filter(appointment=appointment_id).values_list('status')
            
            #appointment already assigned -> move status
            if sales.count() > 0:
                for sale in sales:
                    print(sale[0])
            #appointment not assign -> get random tech -> set status to working
            else:   
                print('no')        
    def open_slots(**kargs):
        if len(kargs) == 1:      # Initialize timeslot for new day (by date)
            date = kargs['date']
            process = _Process(date)
            techs_timeslots = process._get_time_scheduled_techs()
            fieldname_list = collect_time_fieldname (9, 0, [32])
            # tech = [0: email, 1: time_In, 2: time_Out]
            for tech in techs_timeslots:
                delta_In = datetime.combine(datetime.today(), tech[1])
                delta_Out = datetime.combine(datetime.today(), tech[2])
                duration = (int)((delta_Out - delta_In).total_seconds())
                count = math.ceil(duration / (60 * 15))
                if count == 32:
                    for field in fieldname_list:
                        assign = timeSlots.objects.get (tech=tech[0], date=date)
                        setattr (assign, field, True)
                        assign.save ( )
                        logger.info(f'{field} in {tech[0]} is set')
                else:
                    hour_In = tech[1].hour
                    minute_In = tech[1].minute
                    customfield_list = collect_time_fieldname (hour_In, minute_In, [count])
                    for field in customfield_list:
                        assign = timeSlots.objects.get (tech=tech[0], date=date)
                        setattr (assign, field, True)
                        assign.save ( )
                        logger.info(f'{field} in {tech[0]} is set')

class _Process:
    def __init__(self, check_date, appointment_id=None):
        # self.current_date = date.today()
        self.current_date = check_date
        self.dayOfWeek = calendar.day_name[self.current_date.weekday ( )]
        self.dayOfWeek_field_name = "{0}_availability".format (
            calendar.day_name[self.current_date.weekday ( )].lower ( )
        )  # string concat to match field_name for filter

        self.tech = "jlizarraga@unomaha.edu"    #FOR TESTING
        if appointment_id is not None:
            try:
                self.__appointment_id = appointment_id
                self.starttime_object = (Appointment.objects.filter (
                    id=appointment_id, date=self.current_date
                ).values_list ('start_time', flat=True))[0]
                tech_id = Appointment.objects.filter (
                    id=self.__appointment_id, date=check_date  # change date=self.current_date
                ).values_list('technician_id', flat=True)[0]
                self.tech = User.objects.filter(id=
                            Technician.objects.filter(id=tech_id)
                            .values_list('user', flat=True)[0]).values_list('email', flat=True)[0]
                Technician.objects.filter(id=tech_id).values_list('user', flat=True)[0]
                
            except IndexError:
                msg = f"Appointment id {appointment_id} in {check_date} is not found!!"
                print(msg)

    # CONSIDERING: -remove- scheduled is not always correct to based on
    def _get_time_scheduled_techs(self):
        timeIn_field_name = "{0}_time_In".format (self.dayOfWeek.lower())
        timeOut_field_name = "{0}_time_Out".format (self.dayOfWeek.lower())

        # filter {field_name(provide as custom string): True} (dict)
        time_scheduled = list(TechnicianSchedule.objects.filter (
            **{self.dayOfWeek_field_name: True}
        ).values_list ('tech', timeIn_field_name, timeOut_field_name))

        return time_scheduled

    # DEFINITELY: -keep- all techs (either scheduled or not) always has a timeslot
    #need FIX if -remove- _get_time_scheduled_techs
    def _get_techs_timeslots(self):
        # (0: tech email; 1: timeIn; 2: timeOut)
        time_scheduled = self._get_time_scheduled_techs()
        techs_email = []
        for t in time_scheduled:
            techs_email.append(t[0])

        # get all techs' timeslots 
        time_slots = list ((timeSlots.objects.filter (
            tech=email, date=self.current_date
            ).values ( )[0]) for email in techs_email)

        # return only chosen tech timeslots
        for slots in time_slots:
            if slots['tech'] == self.tech:
                return slots

    # DEFINITELY: -fix-
    #this def should not create sale
    def _assign_chosen_tech(self, tech_email, sale_service):
        # count number of timefield for each service
        count = []
        for _ in sale_service:
            count.append (math.ceil (_['duration'].seconds / (60 * 15)))

        # get slot field_name as start
        hour = self.starttime_object.hour
        minute = self.starttime_object.minute

        # Prepare all timeslot fieldname depend for total duration of all services
        fieldname_list = collect_time_fieldname (hour, minute, count)
        '''
        for i in count:
            # print("move slot:")
            for _ in range (i):
                if minute + 15 >= 60:
                    minute = 0
                    hour += 1
                else:
                    minute += 15
                fieldname_list.append (convert_time_fieldname (hour, minute))
        '''

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

        return tech_email

    # DEFINITELY: -fix- 
    #_split_appointment_to_sales need to actually create sale in the database
    #which REQUIRE service and tech (random or chose)
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


def collect_time_fieldname(starthour, startminute, count: list):
    # move minute back 15 to include the startslot at next count
    startminute -= 15

    fieldname_list = []
    for i in count:
            for _ in range (i):
                if startminute + 15 >= 60:
                    startminute = 0
                    starthour += 1
                else:
                    startminute += 15
                fieldname_list.append (convert_time_fieldname (starthour, startminute))
    return fieldname_list

def convert_time_fieldname(hour, minute):
    hour_string = num_to_word[hour]
    minute_tostring = ("00_" if minute == 0 else str (minute))
    meridiem = ("am" if hour < 12 else "pm")

    return f"{hour_string}{minute_tostring}{meridiem}"


def main():
    pass

if __name__ == 'main':
    main()

#Code snippets for later use
'''
# Find technician who open to do all services in appointment
tech_email = None
for tech in all_time_slots:
    count = 0
    for field in fieldname_list:
        count += (1 if tech[field] == True else 0)
    if count == len (fieldname_list):
        tech_email = tech['tech']
    break
'''
