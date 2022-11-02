from django.shortcuts import render

from Appointments.models import Appointment
from Account.models import User

# Create your views here.
def home(request):
    
    appointment_list = Appointment.objects.all()
    
    appointment_list = Appointment.objects.all().values_list('customer', 'start_time', 'end_time', 'totalCharge', 'id')

    appointment_arr = []
    for a in appointment_list:
        appointment = list(a)
        appointment[0] = User.objects.filter(id=a[0]).values_list("first_name", "last_name")[0]
        appointment_arr.append(appointment)
        
    return render(request, 'home.html', {
        'appointments': appointment_arr,
    })
