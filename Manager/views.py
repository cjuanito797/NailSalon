import calendar
import datetime
import json
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from .forms import NewTechnicianForm
from Appointments.models import Appointment, Sale, Service
from Account.models import Technician, User
from Scheduling.models import TechnicianSchedule, timeSlots
from Calendar.models import calendarEntry
import helper.timeslot_process as timeslot_process
from helper.manager_control import C_Appointment, C_Sale, TIME_SLOT
import helper.techs_queue as queue

# Create your views here.
def home(request):
    if request.method == "POST":
        # Appointments Control
        if 'appointment_id' and 'appointment_btn' in request.POST:
            control = C_Appointment(request.POST)
            # INITIALIZE appointment
            if request.POST['appointment_btn'] == 'Initialize':
                frontend_messages(request, control.initialize())
            # CANCEL appointment
            elif request.POST['appointment_btn'] == 'Cancel':
                frontend_messages(request, control.cancel())
            # MODIFY appointment
            else:
                frontend_messages(request, control.modify())
                   
        # Sales Control
        elif 'sale_id' and 'sale_btn' in request.POST:
            control = C_Sale(request.POST)
            # CANCEL sale
            if request.POST['sale_btn'] == 'Cancel':
                frontend_messages(request, control.cancel())
            # TRIGGER sale
            elif request.POST['sale_btn'] == 'Trigger':
                frontend_messages(request, control.trigger())
            # MODIY sale
            else:
                frontend_messages(request, control.modify())
        
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
    status,
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

timetable_date: [date,date,...]

timetable_list:
[{
    tech: {first_name,last_name},
    0: True/False,
    1: True/False,
    ...
    31: True/False
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
    scheduled_techlist = attendance_techlist()
    
    # Time table query
    temp_query = timetable()
    timetable_date = temp_query[0]
    timetable_list = temp_query[1]
    
    
    # include TIMESLOT
    return {
        "apt_date": apt_date_list,
        "appointments": appointment_list,
        "technicians": tech_list,
        "scheduled": scheduled_techlist,
        "timeslots": TIME_SLOT,
        "timetable_date": timetable_date,
        "timetable_list": timetable_list,
        }      


# OTHER MANAGEMENT FUNCTIONS ---------------------------------
def attendance(request):
    if request.method == "POST":
        records = (json.loads(request.POST['data']))["records"]
        print(records)
        for r in records:
            
            hour = r['clocked']['hour']
            min = r['clocked']['min']
            sec = r['clocked']['sec']
            
            milisec = r['clocked']['milisec']
            
            #NEED FIX DATE
            tech_timeslot = timeSlots.objects.get(tech=r['email'], date=datetime.date(2022,12,1))
            tech_timeslot.arrive_time = datetime.time(hour, min, sec, milisec)
            tech_timeslot.save()
            
            #if this run after open time (9:00) then "Append" into _wait Queue with lowest priority
            current_time = datetime.datetime.today()
            open_time = datetime.datetime.combine(datetime.date.today(), datetime.time(9,0,0))
            #if current_time > open_time:
            queue.clock_tech_after_fresh_build(r['email'])
            
        return redirect("manager:home")
    else:
        return redirect("manager:home")
      
def newtech(request):
    if request.method == 'POST':
        form = NewTechnicianForm(request.POST)
        if form.is_valid():
            #print(request.POST['email'])
            all_email = User.objects.all().values_list("email")
            for i in all_email:
                if request.POST['email'] == i[0]:
                    messages.success(request, f"Technician is added successfully!")
                    tmp = dict(request.POST.lists())
                    tech_email = tmp['email'][0]
                    schedule_days = tmp['scheduled_day']        
                    user_obj=User.objects.get(email=tech_email)
                    user_obj.isTechnician=True
                    user_obj.save()
                    
                    a = TechnicianSchedule (tech=tech_email,
                            monday_availability=False,
                            monday_time_In=datetime.time (9, 0),
                            monday_time_Out=datetime.time (17, 0),
                            tuesday_availability=False,
                            tuesday_time_In=datetime.time (9, 0),
                            tuesday_time_Out=datetime.time (17, 0),
                            wednesday_availability=False,
                            wednesday_time_In=datetime.time (9, 0),
                            wednesday_time_Out=datetime.time (17, 0),
                            thursday_availability=False,
                            thursday_time_In=datetime.time (9, 0),
                            thursday_time_Out=datetime.time (17, 0),
                            friday_availability=False,
                            friday_time_In=datetime.time (9, 0),
                            friday_time_Out=datetime.time (17, 0),
                            saturday_availability=False,
                            saturday_time_In=datetime.time (9, 0),
                            saturday_time_Out=datetime.time (17, 0),
                            sunday_availability=False,
                            sunday_time_In=datetime.time (0, 0),
                            sunday_time_Out=datetime.time (0, 0),)
                    a.save()
                    tech_schedule_obj=TechnicianSchedule.objects.get(tech=tech_email)
                    a = Technician(user_id=user_obj.id, bio='', schedule_id=tech_schedule_obj.id, profilePicture=' ')
                    a.save()
                    for i in schedule_days:
                        temp_avai = i+'_availability'
                        setattr(tech_schedule_obj, temp_avai, True)
                        tech_schedule_obj.save()
                        aa = get_date(i)
                        for i in aa:
                            b = timeSlots (tech=tech_email, date=i, arrive_time =None, nine_00_am = True, nine_15am = True, nine_30am = True, 
                                nine_45am = True, ten_00_am = True, ten_15am = True, ten_30am = True, ten_45am = True, eleven_00_am = True, 
                                eleven_15am = True, eleven_30am = True, eleven_45am = True, twelve_00_pm = True, twelve_15pm = True, 
                                twelve_30pm = True, twelve_45pm = True, one_00_pm = True, one_15pm = True, one_30pm = True, one_45pm = True, 
                                two_00_pm = True, two_15pm = True, two_30pm = True, two_45pm = True, three_00_pm = True, three_15pm = True, 
                                three_30pm = True, three_45pm = True, four_00_pm = True, four_15pm = True, four_30pm = True, four_45pm = True)
                            b.save()
                            d = calendarEntry(date=i)
                            d.save()
                            d.technicians.add(Technician.objects.get(user_id=user_obj.id))
                            d.save()
                    

                    
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

# FRONTEND MESSAGES --------------------------------------
def frontend_messages(request, mess: list):
    print(mess)
    if mess[0] == "success":
        for m in mess[1:]:
            messages.success(request, m)
    elif mess[0] == "error":
        for m in mess[1:]:
            messages.error(request, m)
    elif mess[0] == "warning":
        for m in mess[1:]:
            messages.warning(request, m)

# DISPLAY QUERY FUNCTIONS ------------------------------------
def appointments_and_dates_query():
    appointment_query = Appointment.objects.filter(Q(date__gte=datetime.date.today())|Q(date=None)).values(
        'id', 
        'customer', 
        'start_time', 
        'end_time', 
        'totalCharge',
        'date',
        'status'
        )
    appointment_list = []
    apt_date_list = []
    for a in appointment_query:
        if (a['status'] != 'inactive'):
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
                t_email = Technician.objects.get(id=sale['technician']).user
                sale['service'] = Service.objects.filter(id=sale['service']).values_list('name', flat=True)[0]
                sale['technician'] = list(User.objects.filter(email=t_email).values("first_name", "last_name", ))[0]
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

def timetable():
    timetable_query = timeSlots.objects.filter(Q(date__gte=datetime.date.today())|Q(date=None)).values()
    fieldname_list = timeslot_process.collect_time_fieldname (9, 0, datetime.timedelta(hours=8))
    
    timetable_date_list = []
    for timeslot in timetable_query:
        
        if timeslot['date'] not in timetable_date_list:
            timetable_date_list.append(timeslot['date'])
        
        count = 0
        for field in fieldname_list:
            timeslot[count] = timeslot.pop(field)
            count += 1
        timeslot['tech'] = list(User.objects.filter(email=timeslot['tech']).values("first_name", "last_name"))[0]
        del timeslot['id']
        del timeslot['arrive_time']
        
    
    
    return (timetable_date_list, timetable_query)
    
def attendance_techlist():
    wait_queue = queue.get_WAIT_queue()
    work_queue = queue.get_WORK_queue()
    if len(wait_queue)+len(work_queue) <= 0:
        return _get_scheduled_tech()
    else:
        scheduled_techs = _get_scheduled_tech()
        for w in wait_queue:
            for s in scheduled_techs:
                if w[0] == s['email']:
                    scheduled_techs.remove(s)
        for w in work_queue:
            for s in scheduled_techs:
                if w[0] == s['email']:
                    scheduled_techs.remove(s)
        
        return scheduled_techs
                

def _get_scheduled_tech():
    check_date = datetime.date.today()      # INSERT DAY HERE
    current_date = check_date
    dayOfWeek = calendar.day_name[current_date.weekday ( )]
    dayOfWeek_field_name = "{0}_availability".format (
        calendar.day_name[current_date.weekday ( )].lower ( )
    )  # string concat to match field_name for filter
    
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



def get_date(tmp):
    work=[]
    for i in range(30):
        a = (date.today() + datetime.timedelta(days=i))
        b = calendar.day_name[a.weekday()]
        if b.lower() == tmp:
            work.append(a)
    return work