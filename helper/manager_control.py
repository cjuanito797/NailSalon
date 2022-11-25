import datetime
import logging

from Appointments.models import Appointment, Sale, Service
from Account.models import Technician, User
from helper.timeslot_process import Process, get_free_tech, get_timeslot_field_bysale
import helper.techs_queue as techs_queue


TIME_SLOT = {}
# Collect time slot fieldname  
starthour = 9
startmin = -15
for i in range (32):
    if startmin + 15 >= 60:
        startmin = 0
        starthour += 1
    else:
        startmin += 15
    TIME_SLOT[i] = datetime.time(starthour,startmin)



class C_Appointment:
    def __init__(self, post: dict) -> list:
        a_btn = post['appointment_btn']
        self.appointment_id = int(post['appointment_id'])
        #self.sale_list = list(Sale.objects.filter(appointment_id=self.appointment_id)
         #                   .values("id"))
        self.sale_list = Sale.objects.filter(appointment_id=self.appointment_id).values('id', 'status')
        
        if a_btn == 'Modify':
            if post['technician_id'] != "none":
                self.tech_id = int(post['technician_id'])
            else:
                self.tech_id = None
            self.timeslot = int(post['timeslot'])
        
    def initialize(self):
        return_mess = []
        
        # If appointment contain sale => appointment has tech
        if len(self.sale_list) > 0:
            # {'working': 0, 'closed': 0, 'canceled': 0}
            result = Process.close_slots(id=self.appointment_id)
            return_mess.append("Appointment is already triggered!")
            return_mess.append(f"Working sales: {result['working']}")
            return_mess.append(f"Closed sales: {result['closed']}")
            return_mess.append(f"Canceled sales: {result['canceled']}")
            return return_mess
        
        # no sale => need to generate next random tech
        else:
            try:
                assigned_techs = Process.close_slots(id=self.appointment_id)
                return_mess.append("success")
                for tech in assigned_techs:
                    return_mess.append(f"{tech} is assigned to appointment!")
                return return_mess
            except:
                logging.exception("message")
                return_mess.append("error")
                return_mess.append(f"Error! Initialize appointment failed!")
                return return_mess

    def modify(self):
        appointment_obj = Appointment.objects.get(id=self.appointment_id)
        
        
        return_mess = []
        # If appointment links to sales, then not alow to modify
        if len(self.sale_list) > 0:
            return_mess = ["error", f'Appointment is already initialized. Cannot Modify!']
        # If no sale, then modified appointment
        else:
            update_duration = get_total_appointment_duration(self.appointment_id)
            starttime = Appointment.objects.get(id=2).start_time
            starttime = datetime.datetime.combine(datetime.date.today(), starttime)
            endtime = (starttime + update_duration).time()
            # If user did not include technician in modify request, then only modify time
            if self.tech_id is None:
                appointment_obj.start_time = TIME_SLOT[self.timeslot]
                appointment_obj.end_time = endtime
                appointment_obj.totalDuration = update_duration
                appointment_obj.save()
                return_mess.append('success')
                return_mess.append( f'Appointment is modifed with start time at {TIME_SLOT[self.timeslot]}')
            
            # If user included technician in modify request, then add technician in appointment and create sales
            else:
                tech_obj = Technician.objects.get(id=self.tech_id)
                try:
                    appointment_obj.technician = tech_obj
                    appointment_obj.start_time = TIME_SLOT[self.timeslot]
                    appointment_obj.end_time = endtime
                    appointment_obj.totalDuration = update_duration
                    appointment_obj.save()
                    
                    assigned_techs_list = Process.close_slots(id=self.appointment_id)
                    
                    return_mess.append('success')
                    return_mess.append( f'Appointment is modifed. Start time at {TIME_SLOT[self.timeslot]}')
                    for a in assigned_techs_list:
                        return_mess.append( f"{a} is assigned to all sales in appointment.")
                except:
                    return_mess.append( "error")
                    return_mess.append(f"Error! Modifying appointment is failed!")
        return return_mess
        
    def cancel(self):
        return_mess = []
        
        # If appointment contain sale => turn all sales with status different than [closed]
        # to canceled
        if len(self.sale_list) > 0:
            cancel_count = 0
            closed_count = 0
            for s in self.sale_list:
                sale = Sale.objects.get(id=s['id'])
                if sale.status != 'closed':
                    sale.status = 'canceled'
                    sale.save()
                    cancel_count += 1
                else:
                    closed_count += 1
            # {'working': 0, 'closed': 0, 'canceled': 0}
            return_mess.append("Working sales: 0")
            return_mess.append(f"Closed sales: {closed_count}")
            return_mess.append(f"Canceled sales: {cancel_count}")
            
        
        # no sale => delete that appointment
        else:
            Appointment.objects.filter(id=self.appointment_id).delete()
            return_mess.append("Appointment is deleted!")
            
        return return_mess
        
    
class C_Sale:
    def __init__(self, post: dict) -> None:
        s_btn = post['sale_btn']
        
        if s_btn == 'Modify':
            self.sale_obj = Sale.objects.get(id=int(post['sale_id']))
            if post['technician_id'] == "random":
                self.tech_id = post['technician_id']
            elif post['technician_id'] == "none":
                self.tech_id = None
            else:
                self.tech_id = int(post['technician_id'])
        elif s_btn == 'Cancel':
            self.sale_obj = Sale.objects.get(id=int(post['sale_id']))
        else:
            self.appointment_id = int(post['appointment_id'])
            self.sale_id = int(post['sale_id'])
        
    def modify(self):
        return_mess = []
        # If user want to modify a sale with status scheduled
        if self.sale_obj.status == 'scheduled':
            # user provided tech to replace, then assign new tech and give back timeslot for old tech
            if isinstance(self.tech_id, int) or self.tech_id == "random":
                appointment_date = self.sale_obj.appointment.date
                old_technician = self.sale_obj.technician
                sale_duration = self.sale_obj.service.duration
                
                # user choose to replace random tech, then assign tech in wait and give back timeslot for old tech
                if self.tech_id == "random":
                    fieldname_list =  get_timeslot_field_bysale(self.sale_obj.start_time, self.sale_obj.service.duration)
                    
                    tech_email = get_free_tech(appointment_date, fieldname_list, [old_technician.user.email])
                    
                    user_obj = User.objects.get(email=tech_email)
                    self.sale_obj.technician = Technician.objects.get(user=user_obj)
                    self.sale_obj.save()
                else:
                    self.sale_obj.technician = Technician.objects.get(id=self.tech_id)
                    self.sale_obj.save()
                
                # Process.open_slots return structure:
                # [oldtech_email, newtech_email]
                process_returnlist = Process.open_slots(oldtech_id=old_technician.id,
                                                    newtech_id=self.sale_obj.technician.id,
                                                    duration=sale_duration, 
                                                    starttime=self.sale_obj.start_time,
                                                    date=appointment_date)
                old_technician = User.objects.get(email=process_returnlist[0])
                new_technician = User.objects.get(email=process_returnlist[1])
                
                return_mess.append("success")
                return_mess.append("Sale is modified!")
                return_mess.append(f"{old_technician.first_name} {old_technician.last_name} timeslot are returned back! ")
                return_mess.append(f"{new_technician.first_name} {new_technician.last_name} timeslot is closed for sale!")
                
            # user choose to "none" as tech option
            else:
                return_mess.append("warning")
                return_mess.append("Need to provide a technician in order to modify sale!")
                
        else:
            return_mess.append("error")
            return_mess.append("Sale's status is not allow to be modify!")
        return return_mess

    def cancel(self):
        return_mess = []
        
        # If appointment status is [scheduled, working], set status to cancel
        if self.sale_obj.status != 'closed':
            self.sale_obj.status = 'canceled'
            self.sale_obj.save()
            return_mess.append("success")
            return_mess.append("Sale is canceled!")
        else:
            return_mess.append("error")
            return_mess.append("Sale is already closed. Cannot cancel!")
        return return_mess
    
    def trigger(self):
        return_mess = []
        
        result = Process.close_slots(appointment_id=self.appointment_id, sale_id=self.sale_id)
        return_mess.append("success")
        return_mess.append(f"Working sales: {result['working']}")
        return_mess.append(f"Closed sales: {result['closed']}")
        return_mess.append(f"Canceled sales: {result['canceled']}")
        return return_mess



def get_total_appointment_duration(appointment_id):
    duration = datetime.timedelta(0)
    
    sales = Sale.objects.filter(appointment_id=appointment_id)
    for sale in sales:
        duration += sale.service.duration
        
    return duration
        
    