from django.shortcuts import render

from Appointments.models import Appointment

# Create your views here.
def home(request):
    # appointment_list = Appointment.objects.all().values_list("customer", "start_time", "end_time", "totalCharge")
    appointment_list = Appointment.objects.all()
    return render(request, 'home.html', {
        'appointment': appointment_list,
    })