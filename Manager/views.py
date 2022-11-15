import calendar
import datetime
import json
from webbrowser import get
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import NewTechnicianForm
from Appointments.models import Appointment, Sale, Service
from Account.models import Technician, User
from Scheduling.models import TechnicianSchedule, timeSlots

from helper.timeslot_process import Process
from helper.manager_control import C_Appointment, C_Sale, TIME_SLOT

# Create your views here.
def home(request):
    if request.method == "POST":
        #print(request.POST)
        
        if 'appointment_id' and 'appointment_btn' in request.POST:
            control = C_Appointment(request.POST)
            
            if request.POST['appointment_btn'] == 'Trigger':
                mess = control.trigger()
                for m in mess:
                   messages.success(request, m)
            elif request.POST['appointment_btn'] == 'Cancel':
                mess = control.cancel()
                print(mess)
            else:
                mess = control.modify()
                for m in mess:
                   messages.success(request, m)
                   
        elif 'sale_id' and 'sale_btn' in request.POST:
            control = C_Sale(request.POST)
            if request.POST['sale_btn'] == 'Cancel':
                mess = control.cancel()
                print(mess)
            else:
                mess = control.modify()
                for m in mess:
                   messages.success(request, m)
                
        
        return redirect("manager:home")
    else:
        packets = {'packet': display()}
        return render(request, 'home.html', packets)

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
    # Appointment and appointments' Dates Query
    temp_query = appointments_and_dates_query()
    temp_appointment_list = temp_query[0]
    apt_date_list = temp_query[1]
    
    # Sale Query (attach into appointment_list)
    appointment_list = sale_query(temp_appointment_list)

    # Tech Query
    tech_list=tech_query()
    
    # Scheduled Tech
    scheduled_techlist = _get_scheduled_tech()
    
    # include TIMESLOT
    return {
        "apt_date": apt_date_list,
        "appointments": appointment_list,
        "technicians": tech_list,
        "scheduled": scheduled_techlist,
        "timeslots": TIME_SLOT
        }      


# OTHER MANAGEMENT FUNCTIONS ---------------------------------
def attendance(request):
    if request.method == "POST":
        #print(request.POST)
        records = (json.loads(request.POST['data']))["records"]
        for r in records:
            
            hour = r['clocked']['hour']
            min = r['clocked']['min']
            sec = r['clocked']['sec']
            
            milisec = r['clocked']['milisec']
            
            #NEED TO CHANGE DATE
            tech_timeslot = timeSlots.objects.get(tech=r['email'], date=datetime.date(2022,12,11))
            tech_timeslot.arrive_time = datetime.time(hour, min, sec, milisec)
            tech_timeslot.save()
            
        return redirect("manager:home")
    else:
        return redirect("manager:home")
      
def newtech(request):
    if request.method == 'POST':
        form = NewTechnicianForm(request.POST)
        if form.is_valid():
            print(request.POST['email'])
            all_email = User.objects.all().values_list("email")
            for i in all_email:
                if request.POST['email'] == i[0]:
                    messages.success(request, f"Technician is added successfully!")
                    tech_info = request.POST
                    return redirect("manager:home")
            messages.error(request, f"Email \"{request.POST['email']}\" is NOT exist!")
            return redirect("manager:newtech")
        else:
            print(form.errors.as_data())
            messages.error(request, f"Invalid data input!!")
            messages.error(request, f"{str(form.errors.as_data())}")
            return redirect("manager:newtech")
    else:
        form = NewTechnicianForm()
        return render(request, 'newtech.html', {"form":form})

# DISPLAY QUERY FUNCTIONS ---------------------------------
def appointments_and_dates_query():
    appointment_query = Appointment.objects.all().values(
        'id', 
        'customer', 
        'start_time', 
        'end_time', 
        'totalCharge',
        'date'
        )
    appointment_list = []
    apt_date_list = []
    for a in appointment_query:
        a['customer'] = list(User.objects.filter(id=a['customer']).values("first_name", "last_name"))[0]
        appointment_list.append(a)
        if a['date'] not in apt_date_list:
            apt_date_list.append(a['date'])
            
    return (appointment_list, apt_date_list)

def sale_query(appointment_list: list):
    for a in appointment_list:
        s_list = list(Sale.objects.filter(appointment_id=a['id']).values("id", "service", "technician", "status"))
        sale_list = []
        if len(s_list) > 0:
            for sale in s_list:
                sale['service'] = Service.objects.filter(id=sale['service']).values_list('name', flat=True)[0]
                sale['technician'] = list(User.objects.filter(id=sale['technician']).values("first_name", "last_name", ))[0]
                sale['check'] = ''
                sale_list.append(sale)
            sale_list[0]['check'] = "checked"
        a['sales'] = sale_list
        
    return appointment_list

def tech_query():
    tech_query = list(Technician.objects.all().values('id', 'user'))
    tech_list=[]
    for t in tech_query:
        tech = {}
        tech['id'] = t['id']
        u_data = list(User.objects.filter(id=t['user']).values("first_name", "last_name", "email"))[0]
        tech['name'] = {'first_name': u_data['first_name'],'last_name': u_data['last_name']}
        tech['email'] = u_data['email']
        tech_list.append(tech)
        
    return tech_list

def attendance_techlist():
    pass

def _get_scheduled_tech():
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