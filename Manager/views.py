import calendar
import datetime
import json
from webbrowser import get
from django.shortcuts import render, redirect

from Appointments.models import Appointment, Sale, Service
from Account.models import Technician, User
from Scheduling.models import TechnicianSchedule

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
    
# Create your views here.
def home(request):
    if request.method == "POST":
        #print(request.POST)
        
        if 'appointment_id' and 'appointment_btn' in request.POST:
            Control.C_Appointment(request.POST)
        if 'sale_id' and 'sale_btn' in request.POST:
            Control.C_Sale(request.POST)
            
        return redirect("manager:home")
    else:
        packets = {'packet': display()}
        return render(request, 'home.html', packets)

def attendance(request):
    if request.method == "POST":
        #print(request.POST)
        records = (json.loads(request.POST['data']))["records"]
        for r in records:
            print(r)
        return redirect("manager:home")
    else:
        print("bad")
        return redirect("manager:home")


''' # Data return structure
appointment:
[{   id, 
    customer: {first_name,last_name},
    start_time,
    end_time,
    totalCharge,
    sales: [
        id,
        service,
        technician: {first_name,last_name},
        status,
        check,
    ],
}]
    
technician:
[{   id,
    name: {first_name,last_name},
    email,
}]

scheduled:
[{
    email,
    name: {first_name,last_name},
}]
'''

def display():
    # Appointment Query
    appointment_query = Appointment.objects.all().values(
        'id', 
        'customer', 
        'start_time', 
        'end_time', 
        'totalCharge'
        )
    appointment_list = []
    for a in appointment_query:
        a['customer'] = list(User.objects.filter(id=a['customer']).values("first_name", "last_name"))[0]
        appointment_list.append(a)

    # Sale Query (attach into appointment_list)
    for a in appointment_list:
        s_list = list(Sale.objects.filter(appointment_id=7).values("id", "service", "technician", "status"))
        sale_list = []
        if len(s_list) > 0:
            for sale in s_list:
                sale['service'] = Service.objects.filter(id=sale['service']).values_list('name', flat=True)[0]
                sale['technician'] = list(User.objects.filter(id=sale['technician']).values("first_name", "last_name", ))[0]
                sale['check'] = ''
                sale_list.append(sale)
            sale_list[0]['check'] = "checked"
        a['sales'] = sale_list

    # Tech Query
    tech_query = list(Technician.objects.all().values_list('user', flat=True))
    tech_list=[]
    for t in tech_query:
        tech = {}
        tech['id'] = t
        u_data = list(User.objects.filter(id=t).values("first_name", "last_name", "email"))[0]
        tech['name'] = {'first_name': u_data['first_name'],'last_name': u_data['last_name']}
        tech['email'] = u_data['email']
        tech_list.append(tech)
    
    # Scheduled Tech
    scheduled_techlist = get_scheduled_tech()
    
    # include TIMESLOT
    return {
        "appointments": appointment_list,
        "technicians": tech_list,
        "scheduled": scheduled_techlist,
        "timeslots": TIME_SLOT
        }


class Control:
    def __init__(self) -> None:
        pass
    
    class C_Appointment:
        def __init__(self, post: dict) -> None:
            a_btn = post['appointment_btn']
            self.appointment_id = int(post['appointment_id'])
    
            print(f"appointment_id: {self.appointment_id}")
            
            if a_btn == 'Trigger':
                self.trigger()
            elif a_btn == 'Cancel':
                self.cancel()
            else:
                self.modify(int(post['technician_id']), int(post['timeslot']))
            
            
        def trigger(self):
            print("Triggered")

        def modify(self, u_tech_id, timeslot):
            print("Modify")
            print(f'u_tech_id: {u_tech_id}')
            print(f'timeslot: {TIME_SLOT[timeslot]}')
            '''
            tech_id = Technician.objects.filter(user_id=u_tech_id).values_list('id', flat=True)[0]
            Appointment.objects.filter(id=self.appointment_id).update(
                start_time=TIME_SLOT[timeslot],
                technician=tech_id)
            '''

        def cancel(self):
            print("Cancel")
            '''
            sale_count = Sale.objects.filter(appointment=appointment_id).count()
            if sale_count == 0:
                Appointment.objects.filter(id=self.appointment_id).delete()
            '''
        
    class C_Sale:
        def __init__(self, post: dict) -> None:
            s_btn = post['sale_btn']
            self.sale_id = int(post['sale_id'])
            print(f"sale_id: {self.sale_id}")
            
            if s_btn == 'Cancel':
                self.cancel()
            else:
                self.modify(int(post['technician_id']))
            
        def modify(self, u_tech_id):
            print("Modify")
            print(f'u_tech_id: {u_tech_id}')

        def cancel(self):
            print('Cancled')

def get_scheduled_tech():
    check_date = datetime.date.today()      # INSERT DAY HERE
    current_date = check_date
    dayOfWeek = calendar.day_name[current_date.weekday ( )]
    dayOfWeek_field_name = "{0}_availability".format (
        calendar.day_name[current_date.weekday ( )].lower ( )
    )  # string concat to match field_name for filter

    timeIn_field_name = "{0}_time_In".format (dayOfWeek.lower())
    timeOut_field_name = "{0}_time_Out".format (dayOfWeek.lower())

    # filter {field_name(provide as custom string): True} (dict)
    scheduled_tech = list(TechnicianSchedule.objects.filter (
        **{dayOfWeek_field_name: True}
    ).values_list ('tech'))

    scheduled_techlist = []
    for t_email in scheduled_tech:
        t_list = {'email':'', 'name':{}}
        t_list['name'] = list(User.objects.filter(
                email=t_email[0]).values(
                    'first_name','last_name'))[0]
        t_list['email'] = t_email[0]
        scheduled_techlist.append(t_list)
    return(scheduled_techlist)



'''
def display2(id):
    # Query Appointment
    appointment_query = Appointment.objects.all().values_list('customer', 'start_time', 'end_time', 'totalCharge', 'id')
    appointment_list = []
    for a in appointment_query:
        appointment = list(a)
        appointment[0] = User.objects.filter(id=a[0]).values_list("first_name", "last_name")[0]
        if appointment[4] == id:
            appointment.append("checked")
        else:
            appointment.append("")   
        appointment_list.append(appointment)
    # Query Tech    
    tech_query = Technician.objects.all().values_list('user')
    #print(User.objects.filter(id=a[0]).values())
    tech_list = []
    for t in tech_query:
        tech = list(t)
        tech.append(User.objects.filter(id=t[0]).values_list("first_name", "last_name")[0])
        tech_list.append(tech)
    
    sale_list = []  # [ [id,name],[id,first,last],status ]
    if id is None:
        appointment_list[0][5] = "checked"
    else:
    # Query Sale
        sale_query = Sale.objects.filter(appointment=id).values_list("id", "service", "technician", "status")
        
        if len(sale_query) > 0:
            for s in sale_query:
                sale = list(s)    
                sale[1] = Service.objects.filter(id=s[1]).values_list("name", flat=True)[0]
                sale[2] = User.objects.filter(id=s[2]).values_list("first_name", "last_name", )[0]
                sale.append("")
                sale_list.append(sale)
            sale_list[0][4] = "checked"
            
    return {
            "appointments": appointment_list,
            "technicians": tech_list,
            "sales": sale_list,
            "timeslots": TIME_SLOT
            }
''' 

