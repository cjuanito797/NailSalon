import datetime
import json
import math
from timeslot_process import Process
from datetime import date, timedelta, datetime


#appointment = Process.close(date=date(2022, 10, 4), appointment_id=4)


#print(Process.close_slots(id=9,date=date(2022, 12, 10)))
#Process.open_slots(date=date(2022, 11, 5))


#print(appointment)
#for i in appointment:
 #   print(i)
 
 
 
from Appointments.models import Appointment, Sale, Service
from Account.models import Technician, User
from Scheduling.models import TechnicianSchedule, timeSlots
import techs_queue, timeslot_process

import calendar


def main():
    '''
    apt_list = Appointment.objects.get(id=9)
    apt_list.services.add(1)
    
    
    apt_list = Appointment.objects.filter(id=9).values("services")
    print(apt_list)
    '''
    ''' # test _Process
    process = _Process(9)
    techs_queue.wait_to_work(process.assign_tech())
    '''
    
    # build fresh queue for test
    techs_queue.build_fresh_wait_queue(date(2022, 12, 11))
    
    #print(techs_queue.wait_to_work('h@a.com'))
    #print(techs_queue.wait_to_work('f@a.com'))
    
    
    #wait_queue = techs_queue.get_WAIT_queue()
    #work_queue = techs_queue.get_WORK_queue()
    #print(wait_queue)
    #print(work_queue)
    
    '''
    less_prio_wait = wait_queue[-1][1]
    print(less_prio_wait)
    less_prio_work = work_queue[-1][1]
    print(less_prio_work)
    '''
    
    
    
    #tech2 = Appointment.objects.get(id=9)
    #print(tech2.technician.user.email)
    
    
class _Process:
    def __init__(self, appointment_id):
        self.appointment_id = appointment_id
        self.appointment_info = Appointment.objects.filter(id=appointment_id)
        
        # get services' info using services' id list in appointment 
        service_ids = self.appointment_info.values_list ('services', flat=True)
        self.services = []
        for i in service_ids:
            self.services.append (
                (Service.objects.filter (id=i).values ('id', 'duration'))[0]
            )
        self.timeslots_need = self._get_timeslot_field()
        self.free_tech = self._get_free_tech_timeslot()
        
    def assign_tech(self):
        user_obj = User.objects.get(email=self.free_tech)
        # Create new Sales
        for s in self.services:
            Sale.objects.create(
                service=Service.objects.get(id=s['id']),
                technician=Technician.objects.get(user=user_obj),
                appointment=Appointment.objects.get(id=self.appointment_id),
            )
        # Set time slot to False (busy) for open technician
        current_date = self.appointment_info.values_list('date', flat=True)[0]
        assign = timeSlots.objects.get (tech=self.free_tech, date=current_date)
        for field in self.timeslots_need:
            setattr (assign, field, False)
            assign.save ( )
            
        # Attach chosen tech into appointment
        appointment = Appointment.objects.get(id=self.appointment_id)
        appointment.technician = Technician.objects.get(user=user_obj)
        appointment.save()
        
        return self.free_tech
    
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
        fieldname_list = timeslot_process.collect_time_fieldname (hour, minute, count)
        return fieldname_list
        
    def _get_free_tech_timeslot(self):
        for tech, _ in techs_queue.get_WAIT_queue():
            t_timeslot = list(timeSlots.objects.filter(tech=tech, date=date(2022,12,11)).values())[0]
            count = 0
            for slot in self.timeslots_need:
                if t_timeslot[slot] == True:
                    count += 1
            if count == len(self.timeslots_need):
                return tech
    
    def display_init(self):
        print(self.services)
        print(self.timeslots_need)

if __name__ == "__main__":
    main()

            

