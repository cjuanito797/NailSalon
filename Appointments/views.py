import time
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Category
from cart.forms import CartAddServiceForm
from Account.models import Technician
from django.contrib import messages
from Calendar.models import calendarEntry

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
                    # pass in tech to scheduling view, with the tech_id as the argument in the URL.
                    print(tech.user.email)
                    return scheduleWithTech(request, tech.pk)

            else:
                return render(request, "Scheduling/chooseTechnician.html", {'techs': techs})



        return render (request, "Scheduling/chooseTechnician.html", {'techs': techs})

def scheduleWithTech(request, pk):
    # so the pk passed in is the primary key of the tech that we are wanting to schedule with.
    tech = Technician.objects.get(pk=pk)
    workingDays = []
    # this is where we need to do the calculations to get the times that the technician is available depending on day
    # that user has selected.

    # need to get the dates that the technician is actually available on, if not give user to select another technician
    # by taking them back to the previous page.

    availableDates = calendarEntry.objects.all()

    for day in availableDates:
        # if tech is in day, add day to a list.
        # print a list of all technicans working that day.
        techs = day.technicians.all()
        if tech in techs:
            # add the day to a list.
            workingDays.append(day)


    # but our backend algorithm should work to sort technicians by who is available to work on their service the closes and
    # who actually has the most amount of time.

    # so for each day that the user is in our sliding window (remember) only techs available to work on that day get
    # a date entry.

    # so we need to build the time slots, each time that a user has selected on a date.




    return render(request, "Scheduling/calendar.html", {"tech": tech, "availableDates": workingDays})
