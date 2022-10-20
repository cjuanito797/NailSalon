import time
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Category
from cart.forms import CartAddServiceForm
from Account.models import Technician
from django.contrib import messages
from Calendar.models import calendarEntry
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from cart.context_processors import Cart
from Scheduling.models import timeSlots

@never_cache
@cache_control (no_cache=True, must_revalidate=True, no_store=True)
@login_required (login_url='/login/')
def service_list(request, category_slug=None):
    # function that will be used to display oll of our services.
    category = None
    categories = Category.objects.all ( )
    services = Service.objects.all ( )
    techs = Technician.objects.all ( )
    if category_slug:
        category = get_object_or_404 (Category, slug=category_slug)
        services = services.filter (category=category)

    return render (request,
                   'shop/service_list.html',
                   {
                       'category': category,
                       'categories': categories,
                       'services': services,
                       'techs': techs,

                   })


@never_cache
@cache_control (no_cache=True, must_revalidate=True, no_store=True)
@login_required (login_url='/login/')
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


@never_cache
@cache_control (no_cache=True, must_revalidate=True, no_store=True)
@login_required (login_url='/login/')
def appointment_create(request):
    # on this page we will display the technicians on the backend and calculate everything
    # on the backend to pass into our scheduling module, such as total time.

    # display a list of technicians irregardless of who works when and where.
    if request.user.is_authenticated:
        techs = Technician.objects.all ( )
        if request.method == "POST":
            if "technician" in request.POST:
                selectedTech = request.POST.get ("technician")
                tech = Technician.objects.get (pk=selectedTech)

                # so we go the technician that the user has selected.

                # we need to get their first availble day in order to pass to the calendar view page.

                availableDates = calendarEntry.objects.all ( )

                for day in availableDates:

                    techs = day.technicians.all ( )
                    if tech in techs:
                        # we want to get the next immediate date that the technician is available.
                        # also instead of passing in the exact date, we can pass in its ID from the calendar Entry

                        date = day.id
                        return redirect ('appointments:schedule', pk=tech.id, date=day.id)

        # so we display all of the technicians, here not much else to do but handle
        # the choose for me option.

    return render (request, "Scheduling/chooseTechnician.html", {'techs': techs})


@never_cache
@cache_control (no_cache=True, must_revalidate=True, no_store=True)
@login_required (login_url='/login/')
def scheduleWithTech(request, pk, date):
    # so the pk passed in is the primary key of the tech that we are wanting to schedule with.
    tech = Technician.objects.get (pk=pk)
    workingDays = []
    # this is where we need to do the calculations to get the times that the technician is available depending on day
    # that user has selected.

    # need to get the dates that the technician is actually available on, if not give user to select another technician
    # by taking them back to the previous page.

    availableDates = calendarEntry.objects.all ( )

    for day in availableDates:
        # if tech is in day, add day to a list.
        # print a list of all technicans working that day.
        techs = day.technicians.all ( )
        if tech in techs:
            # add the day to a list.
            workingDays.append (day)

    # build a list for the time slots that the user may elect to start their appointment at.

    # some calculations and logic will be written here, keep in mind that we are not actually passing in the date but the ID.

    dateSelected = calendarEntry.objects.get (pk=date)
    print ("You have elected the following date: ", dateSelected.date)

    # so we need to set a default date, make it be the first one in the list, and display the available times.
    # and perform those calculations before we may go with refreshing the page and displaying them.

    # first we need to iterate through the cart and get the total time and multiply by 15.
    cart = Cart (request)

    totalDuration = 0

    for item in cart:
        qty = item['quantity']
        service = Service.objects.get (name=item['service'])

        # goal is to multiply the qty by the estimated duration of that service.
        duration = service.duration

        # we will need to convert the duration into a raw integer.
        durationInMin = (duration.seconds / 60) * qty
        totalDuration += durationInMin

    # divide the total duration to get the time slots that will be required.

    timeslots = (totalDuration / 15)

    # now that we know how many time slots will be required, we can work on getting any availabble start times for that day, by
    # getting the technicians time slot object for the date that was passed in, note that the user won't be able to select a time that
    # the tech is not working on.

    # Now we need to get the time slot data for the date that was passed in.
    timeSlot = timeSlots.objects.get(tech=tech.user.email, date=dateSelected.date)

    # print out the boolean values that are true and determine the various start times for that date.


    # if there are not available start dates, print out an error popup and indicate that the user
    # will need to select another date.

    




    return render (request, "Scheduling/calendar.html", {"tech": tech, "availableDates": workingDays})
