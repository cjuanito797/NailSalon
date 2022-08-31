from django.shortcuts import render
from .models import Technician

# Create your views here.
def home (request):
    techs = Technician.objects.all()
    return render (request, "home.html", {"techs" : techs})

def mainRegister(request):
    return render(request, "home.html")