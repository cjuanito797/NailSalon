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
            
        
            
        return render(request, 'home.html', {
            'appointments': appointment_arr,
        })
