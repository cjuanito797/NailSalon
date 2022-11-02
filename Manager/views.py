from django.shortcuts import render

from .forms import AppointmentID

from Appointments.models import Appointment, Sale
from Account.models import User
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
@csrf_exempt
def home(request):
    if request.method == "POST":
        
        id = (int) (request.POST['appointment'])
        sale_btn = request.POST['sale_btn'] if 'sale_btn' in request.POST else None
        appointment_btn = request.POST['appointment_btn'] if 'appointment_btn' in request.POST else None

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
        
        sale_query = Sale.objects.filter(appointment=id).values_list('technician', 'service')
            
        return render(request, 'home.html', {
            'appointments': appointment_list,
            'sales': sale_query,
        })
        
    else:
        appointment_list = Appointment.objects.all()
        appointment_list = Appointment.objects.all().values_list('customer', 'start_time', 'end_time', 'totalCharge', 'id')
        appointment_arr = []
        for a in appointment_list:
            appointment = list(a)
            appointment[0] = User.objects.filter(id=a[0]).values_list("first_name", "last_name")[0]
            appointment.append("")
            appointment_arr.append(appointment)
        appointment_arr[0][5] = "checked"
            
        return render(request, 'home.html', {
            'appointments': appointment_arr,
        })
        
def trigger():
    pass

def modify():
    pass

def cancel():
    pass
