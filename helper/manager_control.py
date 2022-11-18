import datetime

from Appointments.models import Appointment, Sale, Service
from Account.models import Technician
from helper.timeslot_process import Process


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
            self.tech_id = int(post['technician_id'])
            self.timeslot = int(post['timeslot'])
        
    def trigger(self):
        return_mess = []
        
        # If appointment contain sale => appointment has tech
        if len(self.sale_list) > 0:
            # {'working': 0, 'closed': 0, 'canceled': 0}
            result = Process.close_slots(id=self.appointment_id)
            return_mess.append(f"Working sales: {result['working']}")
            return_mess.append(f"Closed sales: {result['closed']}")
            return_mess.append(f"Canceled sales: {result['canceled']}")
            return return_mess
        
        # no sale => need to generate next random tech *****
        else:
            result = Process.close_slots(id=self.appointment_id)
            return_mess.append(f"{result} is assigned to appointment!")
            return return_mess

    def modify(self):

        appointment_obj = Appointment.objects.get(id=self.appointment_id)
        tech_obj = Technician.objects.get(id=self.tech_id)

        return_mess = []
        # If appointment links to sales, then modified all sales too
        if len(self.sale_list) > 0:
            appointment_obj.technician = tech_obj
            appointment_obj.start_time = TIME_SLOT[self.timeslot]
            appointment_obj.save()
            count = 0
            for s in self.sale_list:
                sale_obj = Sale.objects.get(id=s['id'])
                sale_obj.technician = tech_obj
                sale_obj.save()
                count += 1
            return_mess = [f'Appointment is modifed. {count} sale(s) have been modified.']
        # If no sale, then modified appointment then, split into sales
        else:
            #retrieve services' id attach in appointment
            service_ids = Appointment.objects.filter (
                id=self.appointment_id).values_list (
                    'services', flat=True)
            #get service info for each id 
            count = 0
            for si in service_ids:
                Sale.objects.create(
                    service=Service.objects.get(id=si),
                    technician=tech_obj,
                    appointment=appointment_obj
                )
                count += 1
            return_mess.append( f'Appointment is modifed. {count} sale(s) are created.')
        
        return return_mess
        
    def cancel(self):
        print("Appointment Cancel")
        return_mess = []
        
        # If appointment contain sale => turn all sales status to canceled
        if len(self.sale_list) > 0:
            cancel_count = 0
            for s in self.sale_list:
                sale = Sale.objects.get(id=s['id'])
                sale.status = 'canceled'
                sale.save()
                cancel_count += 1
            # {'working': 0, 'closed': 0, 'canceled': 0}
            return_mess.append("Working sales: 0")
            return_mess.append(f"Closed sales: 0")
            return_mess.append(f"Canceled sales: {cancel_count}")
            
        
        # no sale => delete that appointment
        else:
            Appointment.objects.filter(id=self.appointment_id).delete()
            return_mess.append("Appointment is deleted!")
            
        return return_mess
        
    
class C_Sale:
    def __init__(self, post: dict) -> None:
        s_btn = post['sale_btn']
        self.sale_obj = Sale.objects.get(id=int(post['sale_id']))
        
        if s_btn == 'Modify':
            self.tech_id = int(post['technician_id'])
        
    def modify(self):
        return_mess = []
        if self.sale_obj.status != 'scheduled':
            self.sale_obj.technician = Technician.objects.get(id=self.tech_id)
            self.sale_obj.save()
        
            return_mess.append("Sale is modified!")
        else:
            return_mess.append("Sale's status is not allow to be modify!")
        return return_mess

    def cancel(self):
        return_mess = []
        
        if self.sale_obj.status != 'closed':
            self.sale_obj.status = 'canceled'
            self.sale_obj.save()
            return_mess.append("Sale is canceled!")
        else:
            return_mess.append("Sale is already closed. Cannot cancel!")
            #Sale.objects.filter(id=self.sale_id).delete()
        return return_mess