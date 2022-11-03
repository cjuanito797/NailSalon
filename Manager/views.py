
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from Appointments.models import Appointment, Sale, Service
from Account.models import Technician, User
#from django.views.decorators.csrf import csrf_exempt


# Create your views here.
#@csrf_exempt
def home(request, id=None):
    if request.method == "POST":
        id = (int) (request.POST['appointment_id'])
        
        appointment_control = Control.C_Appointment(request.POST) if 'appointment_btn' in request.POST else None
        sale_control = Control.C_Sale(s_btn=request.POST['sale_btn'], id=id) if 'sale_btn' in request.POST else None
       
        packets = {'packet': display(id)}
        
        return redirect("manager:home_post", id)

    else:
        packets = {'packet': display(id)}
        #print(packets)
        return render(request, 'home.html', packets)


def display(id):
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
    tech_list = []
    for t in tech_query:
        tech = list(t)
        tech.append(User.objects.filter(id=a[0]).values_list("first_name", "last_name")[0])
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
            "sales": sale_list
            }
    
    '''
   {% for service, tech, status, checked in sales %}
                        <input {{ checked }} type="radio" name="sale_id" value="{{ status }}"/>
                        <a>hello</a>
                        <br><br>
                    {% endfor %}
    '''
        
    
class Control:
    def __init__(self) -> None:
        pass
    
    class C_Appointment:
        def __init__(self, post: dict) -> None:
            a_btn = post['appointment_btn']
            appointment_id = post['appointment_id']
            tech_id = post['technician_id']
            
            print(f"appointment: {appointment_id}")
            print(a_btn)
            if a_btn == 'Trigger':
                self.trigger(appointment_id)
            elif a_btn == 'Cancel':
                self.cancel(appointment_id)
            else:
                self.modify(tech_id)
            
        def trigger(self, appointment_id):
            print("Triggered")

        def modify(self, tech_id):
            print(f"tech_id: {tech_id}")

        def cancel(self, appointment_id):
            print("Canceled")
        
    class C_Sale:
        def __init__(self, s_btn, id) -> None:
            self.btn = s_btn
            print(f"sale: {id}")
            print(self.btn)
            if s_btn == 'Cancel':
                pass
            else:
                pass

        def modify():
            pass

        def cancel():
            pass
