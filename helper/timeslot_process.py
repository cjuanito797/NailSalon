import logging
import traceback
import math
import django
import os
import calendar
import datetime
import sys

sys.path.append ("../NailSalon")
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup ( )

from Scheduling.models import TechnicianSchedule, timeSlots
from Appointments.models import Appointment, Service, Sale
from Account.models import Technician, User
from helper import techs_queue as queue

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

num_to_word = {13: 'one_', 14: 'two_', 15: 'three_', 16: 'four_',
               9: 'nine_', 10: 'ten_', 11: 'eleven_',
               12: 'twelve_', }

class Process:
    def close_slots(**kargs):
        if len(kargs) == 2:      # close timeslot by appointment (by appointment_id, sale_id)
            appointment_id = kargs['appointment_id']
            sale = Sale.objects.get(id=kargs['sale_id'])
            if sale.status == 'scheduled':
                sale.status = 'working'
                sale.save()
            if sale.status == 'working':
                sale.status = 'closed'
                sale.save()
            
            return_count = {'scheduled': 0, 'working': 0, 'closed': 0, 'canceled': 0}
            sales = Sale.objects.filter(appointment=appointment_id).values('status')
            for s in sales:
                if s['status'] == 'scheduled':
                    return_count['scheduled'] += 1
                if s['status'] == 'working':
                    return_count['working'] += 1
                if s['status'] == 'closed':
                    return_count['closed'] += 1
                if s['status'] == 'canceled':
                    return_count['canceled'] += 1
            
            if (return_count['closed'] + return_count['canceled']) == len(sales):
                a_obj = Appointment.objects.get(id=appointment_id)
                a_obj.status = "inactive"
                a_obj.save()
                
            return return_count
        
        elif len(kargs) == 1:       # return sale info of a appointment or provide random tech (by id(appointment))  
            appointment_id = kargs['id']
            sales = Sale.objects.filter(appointment=appointment_id).values('id', 'status')
            
            #appointment already assigned -> move status
            if sales.count() > 0:
                return_count = {'scheduled': 0, 'working': 0, 'closed': 0, 'canceled': 0}
                for s in sales:
                    if s['status'] == 'scheduled':
                        #sale = Sale.objects.get(id=s['id'])
                        #sale.status = 'working'
                        #sale.save()
                        return_count['scheduled'] += 1
                    elif s['status'] == 'working':
                        #sale = Sale.objects.get(id=s['id'])
                        #sale.status = 'closed'
                        #sale.save()
                        return_count['working'] += 1
                    elif s['status'] == 'closed':
                        return_count['closed'] += 1
                    elif s['status'] == 'canceled':
                        return_count['canceled'] += 1
                return return_count
            #appointment not assign -> get random tech -> set first sale status to working
            else:   
                process = _Process(appointment_id)
                assigned_tech = process.assign_tech()
                queue.wait_to_work(assigned_tech)
                return assigned_tech
                        
    def open_slots(**kargs):
        if len(kargs) == 1:      # Initialize timeslot for new day (by date)
            date = kargs['date']
            process = _Process_openslot(date)
            techs_timeslots = process._get_time_scheduled_techs()
            fieldname_list = collect_time_fieldname (9, 0, [32])
            # tech = [0: email, 1: time_In, 2: time_Out]
            for tech in techs_timeslots:
                delta_In = datetime.datetime.combine(datetime.datetime.today(), tech[1])
                delta_Out = datetime.datetime.combine(datetime.datetime.today(), tech[2])
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
    def __init__(self, appointment_id):
        self.appointment_id = appointment_id
        self.appointment_info = Appointment.objects.filter(id=appointment_id)
        
        #get services' info by service id list attached in appointment 
        service_ids = self.appointment_info.values_list ('services', flat=True)
        self.services = []
        for i in service_ids:
            self.services.append (
                (Service.objects.filter (id=i).values ('id', 'duration'))[0]
            )
        #get all timeslot need to complete appointment (estimate)
        self.timeslots_need = self._get_timeslot_field()
        #if no technician attached in appointment -> get random tech. Else, use that tech
        if (Appointment.objects.get(id=appointment_id).technician) is None:
            self.tech = self._get_free_tech_timeslot()
        else:
            self.tech = Appointment.objects.get(id=appointment_id).technician.user.email
        
    def assign_tech(self):
        user_obj = User.objects.get(email=self.tech)
        # Create new Sales (first sale status is working; others will be scheduled)
        for index,s in enumerate(self.services):
            if (index == 0):
                Sale.objects.create(
                    service=Service.objects.get(id=s['id']),
                    technician=Technician.objects.get(user=user_obj),
                    appointment=Appointment.objects.get(id=self.appointment_id),
                    status="working",
                )
            else:
                Sale.objects.create(
                    service=Service.objects.get(id=s['id']),
                    technician=Technician.objects.get(user=user_obj),
                    appointment=Appointment.objects.get(id=self.appointment_id),
                    status="scheduled",
                )
        # Set time slot to False (busy) for open technician
        current_date = self.appointment_info.values_list('date', flat=True)[0]
        assign = timeSlots.objects.get (tech=self.tech, date=current_date)
        for field in self.timeslots_need:
            setattr (assign, field, False)
            assign.save ( )
            
        # Attach chosen tech into appointment
        appointment = Appointment.objects.get(id=self.appointment_id)
        appointment.technician = Technician.objects.get(user=user_obj)
        appointment.save()
        
        return self.tech
    
    def _get_timeslot_field(self):
        
        # count number of timefield for each service
        count = []
        for _ in self.services:
            count.append (math.ceil (_['duration'].seconds / (60 * 15)))

        starttime = (self.appointment_info.values_list ('start_time', flat=True))[0]
        # get slot field_name as start
        hour = starttime.hour
        minute = starttime.minute

        # Prepare all timeslot fieldname depend for total duration of all services
        fieldname_list = collect_time_fieldname (hour, minute, count)
        return fieldname_list
        
    def _get_free_tech_timeslot(self):
        for tech, _ in queue.get_WAIT_queue():
            t_timeslot = list(timeSlots.objects.filter(tech=tech, date=datetime.datetime.today()).values())[0]
            count = 0
            for slot in self.timeslots_need:
                if t_timeslot[slot] == True:
                    count += 1
            if count == len(self.timeslots_need):
                return tech

class _Process_openslot:
    def __init__(self, date):
        self.current_date = date
        
    def _get_time_scheduled_techs(self):
        dayOfWeek = calendar.day_name[self.current_date.weekday ( )]
        dayOfWeek_field_name = "{0}_availability".format (
            calendar.day_name[self.current_date.weekday ( )].lower ( )
        )  # string concat to match field_name for filter

        timeIn_field_name = "{0}_time_In".format (dayOfWeek.lower())
        timeOut_field_name = "{0}_time_Out".format (dayOfWeek.lower())

        # filter {field_name(provide as custom string): True} (dict)
        time_scheduled = list(TechnicianSchedule.objects.filter (
            **{dayOfWeek_field_name: True}
        ).values_list ('tech', timeIn_field_name, timeOut_field_name))

        return time_scheduled






class _Process_NOUSE:
    def __init__(self, check_date, appointment_id=None):
        # self.current_date = date.today()
        self.current_date = check_date
        self.dayOfWeek = calendar.day_name[self.current_date.weekday ( )]
        self.dayOfWeek_field_name = "{0}_availability".format (
            calendar.day_name[self.current_date.weekday ( )].lower ( )
        )  # string concat to match field_name for filter

        self.tech = "jlizarraga@unomaha.edu"    #FOR TESTING
        if appointment_id is not None:
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
