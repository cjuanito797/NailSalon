from django.shortcuts import render
from datetime import date
import calendar
from .forms import RegistrationForm
from django.shortcuts import redirect
from .models import Technician
from django.urls import reverse
from django.views.generic import FormView

# Create your views here.
def home(request):
    # print all available technicians for that day.
    curr_date = date.today ( )
    dayOfWeek = calendar.day_name[curr_date.weekday ( )]

    if dayOfWeek == 'Monday':
        techs = Technician.objects.filter(schedule__monday_availability=True)

    elif dayOfWeek == 'Tuesday':
        techs = Technician.objects.filter(schedule__tuesday_availability=True)

    elif dayOfWeek == 'Wednesday':
        techs = Technician.objects.filter(schedule__wednesday_availability=True)

    elif dayOfWeek == 'Thursday':
        techs = Technician.objects.filter(schedule__thursday_availability=True)

    elif dayOfWeek == 'Friday':
        techs = Technician.objects.filter(schedule__friday_availability=True)

    elif dayOfWeek == 'Saturday':
        techs = Technician.objects.filter(schedule__saturday_availability=True)

    else:
        techs = Technician.objects.filter(schedule__sunday_availability=True)




    return render (request, "home.html", {"techs": techs, "dayOfWeek" : dayOfWeek})


class registration_view(FormView):
    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect(reverse('account:home'))
        return render(request, 'registration/registration.html', {'form': form})

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration/registration.html', {'form': form})