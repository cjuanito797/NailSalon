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
import helper.techs_queue as techs_queue

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

num_to_word = {13: 'one_', 14: 'two_', 15: 'three_', 16: 'four_',
               9: 'nine_', 10: 'ten_', 11: 'eleven_',
               12: 'twelve_', }

class Process:
    # "close timeslot" (trigger) by sale (by appointment_id, sale_id)
    def close_slots(**kargs):
        if len(kargs) == 2:      
            appointment_id = kargs['appointment_id']
            sale = Sale.objects.get(id=kargs['sale_id'])
            if sale.status == 'scheduled':
                sale.status = 'working'
                sale.save()
            elif sale.status == 'working':
                sale.status = 'closed'
                sale.save()
            
            # prepare sale info to return
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
            
            # verify all sales in appointment are closed and canceled to set appointment inactive
            if (return_count['closed'] + return_count['canceled']) == len(sales):
                a_obj = Appointment.objects.get(id=appointment_id)
                a_obj.status = "inactive"
                a_obj.save()
                
            return return_count
        
        # close timeslot by appointment (id(appointment))
        elif len(kargs) == 1:      
            appointment_id = kargs['id']
            sales = Sale.objects.filter(appointment=appointment_id).values('id', 'status')
            
            #appointment contain sales -> return sale info in the appointment
            if sales.count() > 0:
                return_count = {'scheduled': 0, 'working': 0, 'closed': 0, 'canceled': 0}
                for s in sales:
                    if s['status'] == 'scheduled':
                        return_count['scheduled'] += 1
                    elif s['status'] == 'working':
                        return_count['working'] += 1
                    elif s['status'] == 'closed':
                        return_count['closed'] += 1
                    elif s['status'] == 'canceled':
                        return_count['canceled'] += 1
                return return_count
            
            #appointment with no sales -> assign different random tech for each sale
            else:   
                process = _Process(appointment_id)
                assigned_tech = process.assign_tech()
                
                return assigned_tech
                        
    def open_slots(**kargs):
        if len(kargs) == 1:      # Initialize timeslot for new day (by date)
            date = kargs['date']
            process = _Process_openslot(date)
            techs_timeslots = process._get_time_scheduled_techs()
            fieldname_list = collect_time_fieldname (9, 0, datetime.timedelta(hours=8))
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
                    customfield_list = collect_time_fieldname (hour_In, minute_In, duration)
                    for field in customfield_list:
                        assign = timeSlots.objects.get (tech=tech[0], date=date)
                        setattr (assign, field, True)
                        assign.save ( )
                        logger.info(f'{field} in {tech[0]} is set')
                        
        # Give back timeslot for technician 
        # parameters need: oldtech_id, newtech_id, duration, starttime, date               
        elif len(kargs) == 5:      
            oldtech_email = Technician.objects.get(id=kargs["oldtech_id"]).user.email
            newtech_email = Technician.objects.get(id=kargs["newtech_id"]).user.email
            oldtech_timeslot_obj = timeSlots.objects.get(tech=oldtech_email, date=kargs["date"])
            newtech_timeslot_obj = timeSlots.objects.get(tech=newtech_email, date=kargs["date"])
            
            duration = kargs["duration"]
            starttime = kargs["starttime"]
            
            fieldname_list = collect_time_fieldname(starttime.hour, starttime.minute, duration)
            for field in fieldname_list:
                setattr (oldtech_timeslot_obj, field, True)
                oldtech_timeslot_obj.save ( )
                logger.info(f'{field} in {oldtech_timeslot_obj} is set')
                
                setattr (newtech_timeslot_obj, field, False)
                newtech_timeslot_obj.save ( )
                logger.info(f'{field} in {newtech_timeslot_obj} is set')
                
            return [oldtech_email, newtech_email]
            
            
            
            
            


class _Process:
    def __init__(self, appointment_id):
        self.appointment_id = appointment_id
        self.appointment_info = Appointment.objects.filter(id=appointment_id)
        self.appointment_date = self.appointment_info.values_list('date', flat=True)[0]
        
        #get services' info by service id list attached in appointment 
        service_ids = self.appointment_info.values_list ('services', flat=True)
        
        '''Services array structure
        [{
            id,
            duration: datetime.timedelta(seconds=),
            startime: datetime.time(hour, minute),
            timeslot: [
                fieldname_slot,
                fieldname_slot,
                ...
            ]
        }]
        
        '''
        self.services = []
        for index, i in enumerate(service_ids):
            self.services.append (
                (Service.objects.filter (id=i).values ('id', 'duration'))[0]
            )
            if index == 0:
                self.services[index]['starttime'] = self.appointment_info.values_list ('start_time', flat=True)[0]
            else:
                next_starttime = (datetime.datetime.combine(datetime.date.today(), self.services[index-1]['starttime']) 
                                  + self.services[index-1]['duration'] ).time()
                self.services[index]['starttime'] = next_starttime
        
    def assign_tech(self):
        #if no technician attached in appointment -> get random tech for each sales, first start working.
        assigned_techs = []
        if (Appointment.objects.get(id=self.appointment_id).technician) is None:
            print(self.services)
            for index, s in enumerate(self.services):
                timeslots_need = get_timeslot_field_bysale(s['starttime'], s['duration'])
                tech = get_free_tech(self.appointment_date, timeslots_need)
                user_obj = User.objects.get(email=tech)
                if index == 0:
                    Sale.objects.create(
                        service=Service.objects.get(id=s['id']),
                        technician=Technician.objects.get(user=user_obj),
                        appointment=Appointment.objects.get(id=self.appointment_id),
                        status="working",
                        start_time=s['starttime'],
                    )
                        
                    # Attach chosen tech into appointment
                    appointment = Appointment.objects.get(id=self.appointment_id)
                    appointment.technician = Technician.objects.get(user=user_obj)
                    appointment.save()
                    # Move tech to work queue
                    techs_queue.wait_to_work(tech)
                    
                else:
                    Sale.objects.create(
                        service=Service.objects.get(id=s['id']),
                        technician=Technician.objects.get(user=user_obj),
                        appointment=Appointment.objects.get(id=self.appointment_id),
                        status="scheduled",
                        start_time=s['starttime'],
                    )
                
                close_timeslot(tech, self.appointment_date, timeslots_need)
                assigned_techs.append(f"{user_obj.first_name} {user_obj.last_name}")
                    
        #if technician is attached in appointment -> apply that tech in all sales
        else:
            tech = Appointment.objects.get(id=self.appointment_id).technician.user.email
            user_obj = User.objects.get(email=tech)
            # Create new Sales (first sale status is working; others will be scheduled)
            for s in self.services:
                Sale.objects.create(
                    service=Service.objects.get(id=s['id']),
                    technician=Technician.objects.get(user=user_obj),
                    appointment=Appointment.objects.get(id=self.appointment_id),
                    status="scheduled",
                    start_time=s['starttime'],
                )
                # Set time slot to False (busy) for open technician
                timeslots_need = get_timeslot_field_bysale(s['starttime'], s['duration'])
                close_timeslot(tech, self.appointment_date, timeslots_need)
            

            assigned_techs.append(f"{user_obj.first_name} {user_obj.last_name}")
            
        return assigned_techs
    

            

    
    def _get_timeslot_field2(self):
        
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



def close_timeslot(tech_email, date, timeslots: list):
    # Set time slot in list to False (busy)
    assign = timeSlots.objects.get (tech=tech_email, date=date)
    for field in timeslots:
        setattr (assign, field, False)
        assign.save ( )

def get_free_tech(sortdate: datetime.date, timeslots_need: list, exclusion: list=[] ):
    waiting_techs = techs_queue.get_WAIT_queue()
    
    # Loop through all waiting
    for tech_email, _ in waiting_techs:         
        # if tech_email in exclusion list then skip               
        if tech_email in exclusion:
            continue                                                #datetime.datetime.today() NEED FIX
        t_timeslot = list(timeSlots.objects.filter(tech=tech_email, date=sortdate).values())[0]
        count = 0
        for slot in timeslots_need:
            if t_timeslot[slot] == True:
                count += 1
        if count == len(timeslots_need):
            return tech_email

def get_timeslot_field_bysale(starttime, duraton):
    # get slot field_name as start
    hour = starttime.hour
    minute = starttime.minute

    # Prepare all timeslot fieldname depend for total duration of all services
    fieldname_list = collect_time_fieldname(hour, minute, duraton)
    return fieldname_list

def collect_time_fieldname(starthour, startminute, duration):
    
    timefield_amount = (math.ceil (duration.seconds / (60 * 15)))
    
    # move minute back 15 to include the startslot at next count
    startminute -= 15

    fieldname_list = []
    for _ in range (timefield_amount):
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

'''
def collect_time_fieldname2(starthour, startminute, count: list):
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
'''




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



'''
        #get services' info by service id list attached in appointment 
        service_ids = self.appointment_info.values_list ('services', flat=True)
        self.services = []
        for i in service_ids:
            self.services.append (
                (Service.objects.filter (id=i).values ('id', 'duration'))[0]
            )
        #get all timeslot need to complete appointment (estimate)
        self.timeslots_need = self._get_timeslot_field()
        '''