from django.shortcuts import render

from .forms import AppointmentID

from Appointments.models import Appointment, Sale
from Account.models import Technician, User
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
@csrf_exempt
def home(request):
    if request.method == "POST":
        
        id = (int) (request.POST['appointment'])
        
        sale_control = Control.C_Sale(s_btn=request.POST['sale_btn']) if 'sale_btn' in request.POST else None
        appointment_control = Control.C_Appointment(a_btn=request.POST['appointment_btn']) if 'appointment_btn' in request.POST else None
        
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
        # Query Sale
        sale_query = Sale.objects.filter(appointment=id).values_list('technician', 'service')
        # Query Tech    
        tech_query = Technician.objects.all().values_list('user')
        tech_list = []
        for t in tech_query:
            tech = list(t)
            tech.append(User.objects.filter(id=a[0]).values_list("first_name", "last_name")[0])
            tech_list.append(tech)
            
        print(tech_list)
        
        return render(request, 'home.html', {
            'appointments': appointment_list,
            'sales': sale_query,
            'technicians': tech_list
        })
        
    else:
        # Query Appointment
        appointment_list = Appointment.objects.all()
        appointment_list = Appointment.objects.all().values_list('customer', 'start_time', 'end_time', 'totalCharge', 'id')
        appointment_arr = []
        for a in appointment_list:
            appointment = list(a)
            appointment[0] = User.objects.filter(id=a[0]).values_list("first_name", "last_name")[0]
            appointment.append("")
            appointment_arr.append(appointment)
        appointment_arr[0][5] = "checked"
        
        # Query Tech    
        tech_query = Technician.objects.all().values_list('user')
        tech_list = []
        for t in tech_query:
            tech = list(t)
            tech.append(User.objects.filter(id=a[0]).values_list("first_name", "last_name")[0])
            tech_list.append(tech)
            
        return render(request, 'home.html', {
            'appointments': appointment_arr,
            'technicians': tech_list,
        })
     

class Control:
    def __init__(self) -> None:
        pass
    
    class C_Appointment:
        def __init__(self, a_btn) -> None:
            self.btn = a_btn
            print("appointment")
            print(self.btn)
            if a_btn == 'Trigger':
                pass
            elif a_btn == 'Cancel':
                pass
            else:
                pass
        
        def trigger():
            pass

        def modify():
            pass

        def cancel():
            pass
        
    class C_Sale:
        def __init__(self, s_btn) -> None:
            self.btn = s_btn
            print("sale")
            print(self.btn)
            if s_btn == 'Cancel':
                pass
            else:
                pass

        def modify():
            pass

        def cancel():
            pass
