import time

from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Category
from cart.forms import CartAddServiceForm
from Account.models import Technician
from django.contrib import messages

def service_list(request, category_slug=None):
    # function that will be used to display oll of our services.
    category = None
    categories = Category.objects.all ( )
    services = Service.objects.all ( )
    if category_slug:
        category = get_object_or_404 (Category, slug=category_slug)
        services = services.filter (category=category)

    return render (request,
                   'shop/service_list.html',
                   {
                       'category': category,
                       'categories': categories,
                       'services': services

                   })


def service_detail(request, id, slug):
    # function used to display the details of a particular service.
    service = get_object_or_404 (Service,
                                 id=id,
                                 slug=slug,
                                 )
    cart_service_form = CartAddServiceForm ( )

    return render (request,
                   'shop/service_detail.html',
                   {
                       'service': service,
                       'cart_service_form': cart_service_form
                   })


def appointment_create(request):
    # on this page we will display the technicians on the backend and calculate everything
    # on the backend to pass into our scheduling module, such as total time.

    # display a list of technicians irregardless of who works when and where.
    if request.user.is_authenticated:
        techs = Technician.objects.all ( )

        # render these objects and depending on which the user selects, pass that into the scheduling and
        # create a dummy appointment model for now.

        # will need to loop through all of the services in the cart and calulcate the total estimated duration.

        # if user selects on option to schedule and a technician was selected, then we need to pass in the tech ID
        # to our calendar module.
        if request.method == 'POST':
            if 'schedule_with' in request.POST:
                myVar = request.POST.get("tech")
                if myVar is None:
                    # render an error message
                    messages.error(request, ('No Technician Was Selected!'))

                else:
                    tech = Technician.objects.get(pk=myVar)


                    print(tech.user.email)

            else:
                return render(request, "Scheduling/chooseTechnician.html", {'techs': techs})



        return render (request, "Scheduling/chooseTechnician.html", {'techs': techs})
