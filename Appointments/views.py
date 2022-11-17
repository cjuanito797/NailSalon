import datetime
import time
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Category, Appointment, Sale
from cart.forms import CartAddServiceForm
from Account.models import Technician
from django.contrib import messages
from Calendar.models import calendarEntry
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from cart.context_processors import Cart
from Scheduling.models import timeSlots
import time
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

globalVar = ""
customerID = 0
technicianID = 0
TotalDurationGlobal = 0
endTimeGlobal = 0
startTimeGlobal = 0
DateGlobal = 0
TotalChargeGlobal = 0


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

    # also pass in the working date to the html page.
    # this is where we need to do the calculations to get the times that the technician is available depending on day
    # that user has selected.

    # need to get the dates that the technician is actually available on, if not give user to select another technician
    # by taking them back to the previous page.

    # this could should only need to be calclated once, when the user selects the technician so I can write this so it only
    # calculates once.

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

    # so we need to set a default date, make it be the first one in the list, and display the available times.
    # and perform those calculations before we may go with refreshing the page and displaying them.

    # first we need to iterate through the cart and get the total time and divide by 15.
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
    timeSlot = timeSlots.objects.get (tech=tech.user.email, date=dateSelected.date)

    # print out the boolean values that are true and determine the various start times for that date.

    # if there are not available start dates, print out an error popup and indicate that the user
    # will need to select another date.

    times = timeSlot.list ( )

    dict = timeSlot.timeDictionary ( )
    temp = iter (list (dict.items ( )))

    x = 32 - timeslots + 1  # used for determining how many start time there can actually be given our reqs.
    # Ex. 4:30 would not be a valid time slot for an appointment require 5 time slots.
    i = 0  # used for iterating over all of the possible start times.
    y = 0  # used for iterating to get the next (n - 1) time slots after a given start time.
    pos = 0  # used for iterating to get the next time slot in the list, gets set to i after each iteration.

    startTimes = []
    startTimesSet = []
    booleanValue = True
    for key, value in dict.items ( ):
        # first we want the actual times that the appointment may be started at.
        # based off of the equation: x - t + 1
        if i < x:
            booleanValue = value
            # transform the list of keys into an array so that we may  iterate through them using index values.
            listForm = list (dict.keys ( ))
            startTimes.append (key)
            # set pos to the value of current key's position.
            pos = i
            # only if all of these values are true may we build a set and add them to a list.
            if value or not (value):  # this is used to get all potential, not assumming whether true or false.
                for y in range (int (timeslots) - 1):
                    pos += 1
                    if (dict.get (listForm[pos])):
                        startTimes.append (listForm[pos])
                    else:
                        # set a second boolean value to false.
                        booleanValue = False
                    y += 1
                pos = 0
                y = 0
                i += 1

            # now only if startTimeTrueOrFal was not false may we add our set of times to a list and clear it always regardless.
            if booleanValue:
                startTimesSet.append (startTimes)
            startTimes = []

    # lastly iterate through our set of starttimes.
    format = '%H:%M%p'
    morningUpperBound = datetime.time (12, 0, 0)
    afternoonUpperBound = datetime.time (15, 0, 0)

    morningTimeSets = []
    afternoonTimeSets = []
    eveningTimeSets = []

    currentDateAndTime = datetime.datetime.now ( ).time ( )
    currentTime = currentDateAndTime.strftime ("%H:%M%p")

    todaysDate = datetime.datetime.today ( ).date ( )
    current_time = datetime.datetime.strptime (currentTime, format)

    for set in startTimesSet:
        datetime_str = datetime.datetime.strptime (set[0], format)
        # only add the times that are logically possible.
        # ex. don't add 9:00am if it is 12pm in the afternoon

        # though we need to convert the time into 24 hour time format in order to do the comparison.
        # now we only need to do this for the today's date.

        time_in24 = datetime.datetime.strptime (set[0], '%I:%M%p')
        if dateSelected.date == todaysDate:
            if time_in24.time ( ) > current_time.time ( ):
                if time_in24.time ( ) < morningUpperBound:
                    morningTimeSets.append (set)
                if time_in24.time ( ) < afternoonUpperBound:
                    if time_in24.time ( ) > morningUpperBound:
                        afternoonTimeSets.append (set)
                else:
                    eveningTimeSets.append (set)
        else:
            if time_in24.time ( ) < morningUpperBound:
                morningTimeSets.append (set)
            if time_in24.time ( ) < afternoonUpperBound:
                if time_in24.time ( ) > morningUpperBound:
                    afternoonTimeSets.append (set)
            else:
                eveningTimeSets.append (set)

    if request.method == "POST":
        if "start_time" in request.POST:
            if request.user.is_authenticated:
                myVar = request.POST.get ("start_time")
                # ok we have the start time, now what we need to do is to setup everything to send to confirmation page.
                # really all that we need to pass in is our Appointment object that we are creating.

                # ultimately if the user decides that they would like to alter it, we can  simply delete it.
                # but we wont alter the time slots until after they have confirmed their appointment.

                startTime = datetime.datetime.strptime (myVar, '%I:%M%p')
                endTime = startTime + datetime.timedelta (minutes=totalDuration)

                # update a global variable with the set of times.
                global globalVar
                for set in startTimesSet:
                    if set[0] == myVar:
                        globalVar = set

                # so one thing that i'm thinking is that we can utilize global variables in order to
                # store this information so that we don't have to pass in parameters
                # and we only create an appointment explicitly when the user has selected "Confirm"

                global customerID
                customerID = request.user.id

                global technicianID
                technicianID = tech.id

                global startTimeGlobal
                startTimeGlobal = startTime.time ( )

                global endTimeGlobal
                endTimeGlobal = endTime.time ( )

                global TotalDurationGlobal
                TotalDurationGlobal = totalDuration

                global DateGlobal
                DateGlobal = dateSelected.date

                global TotalChargeGlobal
                TotalChargeGlobal = cart.get_total_price ( )

                return redirect ('appointments:confirm')

    return render (request, "Scheduling/calendar.html", {"tech": tech, "availableDates": workingDays,
                                                         'morning': morningTimeSets, 'afternoon': afternoonTimeSets,
                                                         'evening': eveningTimeSets, "date": dateSelected.date})


def confirmAppointment(request):
    # so in here we need to render a form, where the user will:
    # provide any additional details that they would like to include in their request.
    # upload any additional images, that they would like for the technician to
    # here we need to render the form and when the user confirms we can set the timeslots to false.

    # first delete said appointment but store it elsewhere.
    if request.method == "POST":
        if "Confirm" in request.POST:

            # clear the cart
            cart = Cart (request)

            new_appointment = Appointment.objects.create (
                customer_id=customerID,
                technician_id=technicianID,

                # iterate through the cart and add the services
                # currently there is no way to add the quantity, we could create a ServiceOrderItem

                start_time=startTimeGlobal,
                end_time=endTimeGlobal,
                totalDuration=TotalDurationGlobal,
                date=DateGlobal,
                totalCharge=TotalChargeGlobal
            )

            new_appointment.save ( )

            # create sale items for each item within the cart
            for item in cart:
                # get the service item, using the item name.
                service = Service.objects.filter (name__exact=item['service']).get ( )
                # create sale items for each item in the cart
                Sale.objects.create (service_id=service.id, technician_id=new_appointment.technician.id,
                                     appointment_id=new_appointment.id, status='scheduled').save ( )

            cart.clear ( )

            # set the appropriate time slots to false
            timeSlot = timeSlots.objects.get (tech=new_appointment.technician.user.email, date=new_appointment.date)
            for time in globalVar:
                slot = timeSlot.getTimeSlot (time)
                setattr (timeSlot, slot, False)

            # build a query set for the sale items that were created for this appointment, to display in the e-mail.

            saleItems = Sale.objects.filter (appointment_id=new_appointment.id).all ( )
            subTotal = TotalChargeGlobal
            grandTotal = new_appointment.getTotalCharge ( )

            timeSlot.save ( )
            plaintext = get_template ('Send/confirmationEmail.txt')
            htmlEmail = get_template ('Send/confirmationEmail.html')

            content = (
                {'username': request.user.first_name, 'date': new_appointment.date, 'time': new_appointment.start_time,
                 'technician': new_appointment.technician.user.first_name, 'saleItems': saleItems, 'subTotal': subTotal,
                 'grandTotal': float ("{:.2f}".format (grandTotal))})

            text_content = plaintext.render (content)
            html_content = htmlEmail.render (content)
            msg = EmailMultiAlternatives ('Your Appointment', html_content, 'cjuangas17@gmail.com',
                                          [request.user.email])
            msg.attach_alternative (html_content, "text/html")
            msg.send ( )

            return redirect ('appointments:confirmation')

    # if the user changes their mind, delete the appointment and return to the calendar page with appropriate params.
    return render (request, "Scheduling/confirmation.html")


def index(request):
    return render (request, "Send/confirmation.html")


def deleteAppointment(request, id):
    appointment = Appointment.objects.filter (pk=id).get ( )
    tech = Technician.objects.filter (pk=appointment.technician.id).get ( )

    # get the time slot data for that technician.
    time_slot = timeSlots.objects.filter (tech=tech.user.email, date=appointment.date).get ( )

    # determine the time slots that we need to free up, similarly to how we set them to false.

    # build a set of the times from the appoointment and convert them to 12-hour.
    startTime = appointment.start_time
    startTime = datetime.datetime.strptime (str (startTime), "%H:%M:%S")
    time = datetime.datetime.strftime (startTime, "%I:%M%p")

    # get the number of time slots required for this appointment
    timeSlotsRequired = appointment.totalDuration / 15

    i = 0
    timeToChange = ""
    for i in range (int (timeSlotsRequired)):
        # print out the time slots for this appointment in 12 hour format.
        print (time.lower ( ))
        timeToChange = time_slot.getTimeSlot (time.lower ( ).lstrip ("0"))
        print ("We are setting", timeToChange, " back to true")
        setattr (time_slot, timeToChange, True)

        # will need to use an offset of 15 minutes, recall how we calculated end_time.
        startTime = startTime + datetime.timedelta (minutes=15)
        time = datetime.datetime.strftime (startTime, "%I:%M%p")

    time_slot.save ( )

    # notify both of the parties involved, about their cancelled appointment.

    # build a context dictionary, of the information that will be e-mailed to the user.

    plaintext = get_template ('Send/userCancellation.txt')
    htmlEmail = get_template ('Send/userCancellation.html')

    content = (
        {'username': request.user.first_name, 'date': appointment.date,
         'technician': appointment.technician.user.first_name, })

    text_content = plaintext.render (content)
    html_content = htmlEmail.render (content)
    msg = EmailMultiAlternatives ('Appointment has been cancelled!', html_content, 'cjuangas17@gmail.com',
                                  [request.user.email])
    msg.attach_alternative (html_content, "text/html")
    msg.send ( )

    # send an e-mail to the technician.
    plaintext = get_template ('Send/technicianCancellation.txt')
    htmlEmail = get_template ('Send/technicianCancellation.html')

    content = (
        {
            'technician': appointment.technician.user.first_name, 'user': request.user.first_name,
            'start_time': appointment.start_time, 'end_time': appointment.end_time, 'date': appointment.date,
            })

    text_content = plaintext.render (content)
    html_content = htmlEmail.render (content)
    msg = EmailMultiAlternatives ('Appointment has been cancelled!', html_content, 'cjuangas17@gmail.com',
                                  [appointment.technician.user.email])
    msg.attach_alternative (html_content, "text/html")
    msg.send ( )

    appointment.delete ( )

    return redirect ('Account:home')
