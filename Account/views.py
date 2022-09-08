from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import date
import calendar

from .forms import LoginForm
from .models import Technician


# Create your views here.
def home(request):
    # print all available technicians for that day.
    curr_date = date.today()
    dayOfWeek = calendar.day_name[curr_date.weekday()]

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

    return render(request, "home.html", {"techs": techs, "dayOfWeek": dayOfWeek})


def mainRegister(request):
    return render(request, "home.html")


def user_login(request):
    form = LoginForm(request.POST)
    if form.is_valid():

        cd = form.cleaned_data
        user = authenticate(request,
                            username=cd['email'],
                            password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(redirect('account:home'))
            else:
                return HttpResponse('Disabled Account')
        else:
            return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'registration/LoginForm.html', {'form': form})
