import datetime
import time
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Category, Appointment, Sale
from cart.forms import CartAddServiceForm
from Account.models import Technician, Customer, User
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
from helper import appointment_queue

globalVar = ""
customerID = 0
technicianID = 0
TotalDurationGlobal = 0
endTimeGlobal = 0
startTimeGlobal = 0
DateGlobal = 0
TotalChargeGlobal = 0
firstName = ""
lastName = ""


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

        # pass in the date so we can call on "choose for me" option for selecting technician.

    today = datetime.date.today ( )
    return render (request, "Scheduling/chooseTechnician.html", {'techs': techs, 'date': today})


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


@never_cache
@cache_control (no_cache=True, must_revalidate=True, no_store=True)
@login_required (login_url='/login/')
def scheduleWithNoneTech(request, date):
    startTimes = []
    startTimesSet = []
    booleanValue = True
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
    days = date
    print(days)
    morningTimeSets = []
    morningTimeSets0 = [
        ['9:00am', '9:15am', '9:30am', '9:45am'],
        ['9:15am', '9:30am', '9:45am', '10:00am'],
        ['9:30am', '9:45am', '10:00am', '10:15am'],
        ['9:45am', '10:00am', '10:15am', '10:30am'],
        ['10:00am', '10:15am', '10:30am', '10:45am'],
        ['10:15am', '10:30am', '10:45am', '11:00am'],
        ['10:30am', '10:45am', '11:00am', '11:15am'],
        ['10:45am', '11:00am', '11:15am', '11:30am'],
        ['11:00am', '11:15am', '11:30am', '11:45am'],
        ['11:15am', '11:30am', '11:45am', '12:00pm'],
        ['11:30am', '11:45am', '12:00pm', '12:15pm'],
        ['11:45am', '12:00pm', '12:15pm', '12:30pm'],
    ]
    afternoonTimeSets=[]
    afternoonTimeSets0 = [
        ['12:00pm','12:15pm', '12:30pm', '12:45pm'],
        ['12:15pm', '12:30pm', '12:45pm', '1:00pm'],
        ['12:30pm', '12:45pm', '1:00pm', '1:15pm'],
        ['12:45pm', '1:00pm', '1:15pm', '1:30pm'],
        ['1:00pm', '1:15pm', '1:30pm', '1:45pm'],
        ['1:15pm', '1:30pm', '1:45pm', '2:00pm'],
        ['1:30pm', '1:45pm', '2:00pm', '2:15pm'],
        ['1:45pm', '2:00pm', '2:15pm', '2:30pm'],
        ['2:00pm', '2:15pm', '2:30pm', '2:45pm'],
        ['2:15pm', '2:30pm', '2:45pm', '3:00pm'],
        ['2:30pm', '2:45pm', '3:00pm', '3:15pm'],
        ['2:45pm', '3:00pm', '3:15pm', '3:30pm'],
    ]
    eveningTimeSets=[]
    eveningTimeSets0 = [
        ['3:00pm', '3:15pm', '3:30pm', '3:45pm'],
        ['3:15pm', '3:30pm', '3:45pm', '4:00pm'],
        ['3:30pm', '3:45pm', '4:00pm', '4:15pm'],
        ['3:45pm', '4:00pm', '4:15pm', '4:30pm'],
        ['4:00pm', '4:15pm', '4:30pm', '4:45pm'],
    ]
    
    workingDays = []

    availableDates = calendarEntry.objects.all ( )

    for day in availableDates:
        workingDays.append (day)
    calendar = calendarEntry.objects.all ( )
    if isinstance(date, int) == False:
        date = calendarEntry.objects.filter (date=date).get ( )
        times = appointment_queue.get_next_frame_available (date.date)
        for i in morningTimeSets0:
            if datetime.datetime.strptime(i[0], "%I:%M%p").time() >= times:
                    morningTimeSets.append(i)
        for i in afternoonTimeSets0:
            if datetime.datetime.strptime(i[0], "%I:%M%p").time() >= times:
                    afternoonTimeSets.append(i)
        for i in eveningTimeSets0:
            if datetime.datetime.strptime(i[0], "%I:%M%p").time() >= times:
                    eveningTimeSets.append(i)

        return render (request, "Scheduling/calendar_none.html", {"tech": None, "availableDates": workingDays,
                                                            'morning': morningTimeSets, 'afternoon': afternoonTimeSets,
                                                    'evening': eveningTimeSets, "date": date.date})
    else:
        dateSelected = calendarEntry.objects.get (pk=date)
        print(days)
        print(type(days))
        times = appointment_queue.get_next_frame_available (dateSelected.date)
        for i in morningTimeSets0:
            if datetime.datetime.strptime(i[0], "%I:%M%p").time() >= times:
                    morningTimeSets.append(i)
        for i in afternoonTimeSets0:
            if datetime.datetime.strptime(i[0], "%I:%M%p").time() >= times:
                    afternoonTimeSets.append(i)
        for i in eveningTimeSets0:
            if datetime.datetime.strptime(i[0], "%I:%M%p").time() >= times:
                    eveningTimeSets.append(i)
        if request.method == "POST":
            if "start_time" in request.POST:
                if request.user.is_authenticated:
                    myVar = request.POST.get ("start_time")

                    startTime = datetime.datetime.strptime (myVar, '%I:%M%p')
                    endTime = startTime + datetime.timedelta (minutes=totalDuration)

                    # update a global variable with the set of times.
                    global globalVar
                    for set in startTimesSet:
                        if set[0] == myVar:
                            globalVar = set
                    global customerID
                    customerID = request.user.id

                    global technicianID
                    technicianID = None

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
        return render (request, "Scheduling/calendar_none.html", {"tech": None, "availableDates": workingDays,
                                                            'morning': morningTimeSets, 'afternoon': afternoonTimeSets,
                                                    'evening': eveningTimeSets, "date": dateSelected.date})
                                                



def confirmAppointment(request):
    if request.method == "POST":
        if "Confirm" in request.POST:

            # clear the cart
            cart = Cart (request)
            if technicianID is not None:
                new_appointment = Appointment.objects.create (
                    customer_id=customerID,
                    technician_id=technicianID,
                    start_time=startTimeGlobal,
                    end_time=endTimeGlobal,
                    totalDuration=TotalDurationGlobal,
                    date=DateGlobal,
                    totalCharge=TotalChargeGlobal
                )
                # add services from cart into appointment

                for item in cart:
                    # get the service item, using the item name.
                    service = Service.objects.filter (name__exact=item['service']).get ( )
                    new_appointment.services.add (service)
                    # create sale items for each item in the cart
                    Sale.objects.create (service_id=service.id, technician_id=new_appointment.technician.id,
                                        appointment_id=new_appointment.id, status='scheduled').save ( )

                new_appointment.save ( )
                cart.clear ( )

                # build a query set for the sale items that were created for this appointment, to display in the e-mail
                subTotal = TotalChargeGlobal
                grandTotal = new_appointment.getTotalCharge ( )

                print("Just finished calculating the totals for your appointment")
                if new_appointment.technician is not None:
                    # set the appropriate time slots to false
                    timeSlot = timeSlots.objects.get (tech=new_appointment.technician.user.email, date=new_appointment.date)
                    for time in globalVar:
                        slot = timeSlot.getTimeSlot (time)
                        setattr (timeSlot, slot, False)
                    timeSlot.save ( )
                    saleItems = Sale.objects.filter (appointment_id=new_appointment.id).all ( )
                    content = (
                        {'username': request.user.first_name, 'date': new_appointment.date,
                        'time': new_appointment.start_time,
                        'technician': new_appointment.technician.user.first_name, 'saleItems': saleItems,
                        'subTotal': subTotal,
                        'grandTotal': float ("{:.2f}".format (grandTotal))})
                else:
                    content = (
                        {'username': request.user.first_name, 'date': new_appointment.date,
                        'time': new_appointment.start_time,
                        'subTotal': subTotal, 'grandTotal': float ("{:.2f}".format (grandTotal))})

                plaintext = get_template ('Send/confirmationEmail.txt')
                htmlEmail = get_template ('Send/confirmationEmail.html')

                text_content = plaintext.render (content)
                html_content = htmlEmail.render (content)
                msg = EmailMultiAlternatives ('Your Appointment', html_content, 'applenailsalon23@gmail.com',
                                            [request.user.email])
                print("Preparing to add the html content to your e-mail.")
                msg.attach_alternative (html_content, "text/html")
                print("HTML content has been attatched, preparing to send your e-mail.")

                msg.send (fail_silently=False)

                print("Message has been sent.")
                return redirect ('appointments:confirmation')
            else:
                new_appointment = Appointment.objects.create (
                    customer_id=customerID,
                    technician_id=technicianID,
                    start_time=startTimeGlobal,
                    end_time=endTimeGlobal,
                    totalDuration=TotalDurationGlobal,
                    date=DateGlobal,
                    totalCharge=TotalChargeGlobal
                )
                # add services from cart into appointment

                for item in cart:
                    # get the service item, using the item name.
                    service = Service.objects.filter (name__exact=item['service']).get ( )
                    new_appointment.services.add (service)
                    # create sale items for each item in the cart
                    
                new_appointment.save ( )
                cart.clear ( )

                # build a query set for the sale items that were created for this appointment, to display in the e-mail
                subTotal = TotalChargeGlobal
                grandTotal = new_appointment.getTotalCharge ( )

                print("Just finished calculating the totals for your appointment")
                if new_appointment.technician is not None:
                    # set the appropriate time slots to false
                    timeSlot = timeSlots.objects.get (tech=new_appointment.technician.user.email, date=new_appointment.date)
                    for time in globalVar:
                        slot = timeSlot.getTimeSlot (time)
                        setattr (timeSlot, slot, False)
                    timeSlot.save ( )
                    saleItems = Sale.objects.filter (appointment_id=new_appointment.id).all ( )
                    content = (
                        {'username': request.user.first_name, 'date': new_appointment.date,
                        'time': new_appointment.start_time,
                        'technician': new_appointment.technician.user.first_name, 'saleItems': saleItems,
                        'subTotal': subTotal,
                        'grandTotal': float ("{:.2f}".format (grandTotal))})
                else:
                    content = (
                        {'username': request.user.first_name, 'date': new_appointment.date,
                        'time': new_appointment.start_time,
                        'subTotal': subTotal, 'grandTotal': float ("{:.2f}".format (grandTotal))})

                plaintext = get_template ('Send/confirmationEmail.txt')
                htmlEmail = get_template ('Send/confirmationEmail.html')

                text_content = plaintext.render (content)
                html_content = htmlEmail.render (content)
                msg = EmailMultiAlternatives ('Your Appointment', html_content, 'applenailsalon23@gmail.com',
                                            [request.user.email])
                print("Preparing to add the html content to your e-mail.")
                msg.attach_alternative (html_content, "text/html")
                print("HTML content has been attatched, preparing to send your e-mail.")

                msg.send (fail_silently=False)

                print("Message has been sent.")
                return redirect ('appointments:confirmation')

    # if the user changes their mind, delete the appointment and return to the calendar page with appropriate params.
    return render (request, "Scheduling/confirmation.html")


def index(request):
    return render (request, "Send/confirmation.html")


def selectCustomer(request):
    # pass in a query set of our customers.
    customers = Customer.objects.all()

    # determine whether attendant selected a registered user or filled out form for a guest user.
    if request.method == 'POST':
        if 'registeredUser' in request.POST:
            user = request.POST.get('userList', None)

            # continue with creation of appointment with the registered user.
            # by passing in the user to an appointment confirmation page and pass in id of user.
            customer = User.objects.filter(email__exact=user).get()

            return redirect('appointments:manager_confirmation', customer.id)

        elif 'guestUser' in request.POST:
            # this indicates that attendant is creating appointment with non-registered user.

            print("So we are doing an appointment for a guest user!")
            global firstName
            firstName = request.POST.get('guest_first_name')

            global lastName
            lastName = request.POST.get('guest_last_name')


            # update global variables with first and last name from form.


            # since there is no param to send to confirmation, we will send in a 0 which means that there does not exist a user.
            return redirect('appointments:manager_confirmation', 0)

    return render (request, 'Scheduling/selectCustomer.html', {'customerList': customers})


def manager_confirmation(request, id):

    # once user has clicked on confirm will appointment be created
    customer = False
    if request.method == "POST":
        if "Confirm" in request.POST:
            if id != 0:
                customer = User.objects.filter (pk=id).get ( )

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


                new_appointment = Appointment.objects.create (
                    customer_id=customer.id,
                    start_time=None,
                    end_time=None,
                    totalDuration=totalDuration,
                    date=datetime.datetime.today().date(),
                    totalCharge=cart.get_total_price(),
                )
                # add services from cart into appointment

                for item in cart:
                    # get the service item, using the item name.
                    service = Service.objects.filter (name__exact=item['service']).get ( )
                    new_appointment.services.add (service)
                    # create sale items for each item in the cart
                    Sale.objects.create (service_id=service.id,technician_id=1,
                                     appointment_id=new_appointment.id, status='scheduled').save ( )

                new_appointment.save ( )
                cart.clear ( )

                # build a query set for the sale items that were created for this appointment, to display in the e-mail
                subTotal = 0
                grandTotal = new_appointment.getTotalCharge ( )

                return redirect('account:home')
            elif id == 0:
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

                new_appointment = Appointment.objects.create (
                    start_time=None,
                    end_time=None,
                    totalDuration=totalDuration,
                    date=datetime.datetime.today ( ).date ( ),
                    totalCharge=cart.get_total_price ( ),
                    guest_first_name=firstName,
                    guest_last_name=lastName,
                )
                # add services from cart into appointment

                for item in cart:
                    # get the service item, using the item name.
                    service = Service.objects.filter (name__exact=item['service']).get ( )
                    new_appointment.services.add (service)
                    # create sale items for each item in the cart
                    Sale.objects.create (service_id=service.id, technician_id=1,
                                         appointment_id=new_appointment.id, status='scheduled').save ( )

                new_appointment.save ( )
                cart.clear ( )

                # build a query set for the sale items that were created for this appointment, to display in the e-mail
                subTotal = 0
                grandTotal = new_appointment.getTotalCharge ( )

                return redirect('account:home')

    return render(request, "Scheduling/managerConfirmation.html", {'customer': customer})

def rescheduleAppointment(request, id, date):
    # get the corresponding appointment, by way of it's id.
    # build a list for the time slots that the user may elect to start their appointment at.

    # some calculations and logic will be written here, keep in mind that we are not actually passing in the date but the ID.

    dateSelected = calendarEntry.objects.get (date=date)
    appointment = Appointment.objects.filter (pk=id).get ( )
    tech = Technician.objects.get (pk=appointment.technician.id)

    # print out the time slots that the appointment is taking up by way of its startTime, endTime and totalDuration / 15.
    startTime = appointment.start_time

    # use strptime function on the startTime.
    startTime = datetime.datetime.strptime (str (startTime), "%H:%M:%S")

    # utilize the strftime function in order to convert time into 12 hour with am/pm.
    time = datetime.datetime.strftime (startTime, "%I:%M%p")

    # get the number of time slots that are required for this appointment.

    # get the number of time slots that, are required for this appointment.
    timeSlotsRequired = appointment.totalDuration / 15

    # create a copy of the timeSlot object that is referenced by this appointment.
    time_slot = timeSlots.objects.filter (date=appointment.date, tech=appointment.technician.user.email).get ( )

    i = 0
    for i in range (int (timeSlotsRequired)):
        # get the time in am/pm and print in lower case.
        timeToChange = time_slot.getTimeSlot (time.lower ( ).lstrip ("0"))
        print ("We are setting", timeToChange, " back to true")
        setattr (time_slot, timeToChange, True)

        # add an offset of 15 minutes to the startTime variable.
        startTime = startTime + datetime.timedelta (minutes=15)
        time = datetime.datetime.strftime (startTime, "%I:%M%p")

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

    x = 32 - timeSlotsRequired + 1  # used for determining how many start times there can actually be given our requirements.
    i = 0  # used for iterating over all the possible start times
    y = 0  # used for iterating to get the next (n - 1) time slots after a given start time.
    pos = 0  # used for iterating to get the next time slot in the list, gets set to i after each iteration.

    startTimes = []
    startTimesSet = []
    booleanValue = True

    timeSlot = timeSlots.objects.get (tech=appointment.technician.user.email,
                                      date=dateSelected.date)  # get the time slot data for the date selected
    if dateSelected.date == appointment.date:
        timeSlot = time_slot

    times = timeSlot.list ( )
    dict = timeSlot.timeDictionary ( )
    temp = iter (list (dict.items ( )))

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
                for y in range (int (timeSlotsRequired) - 1):
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

    if dateSelected.date == datetime.date.today ( ) and dateSelected.date != appointment.date:
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

    elif dateSelected.date == datetime.date.today ( ) and dateSelected.date == appointment.date:
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

    elif dateSelected.date != datetime.date.today ( ) and dateSelected.date == appointment.date:
        for set in startTimesSet:
            datetime_str = datetime.datetime.strptime (set[0], format)
            # only add the times that are logically possible.
            # ex. don't add 9:00am if it is 12pm in the afternoon

            # though we need to convert the time into 24 hour time format in order to do the comparison.
            # now we only need to do this for the today's date.

            time_in24 = datetime.datetime.strptime (set[0], '%I:%M%p')
            if time_in24.time ( ) < morningUpperBound:
                morningTimeSets.append (set)
            if time_in24.time ( ) < afternoonUpperBound:
                if time_in24.time ( ) > morningUpperBound:
                    afternoonTimeSets.append (set)
            else:
                eveningTimeSets.append (set)

    elif dateSelected.date != datetime.date.today ( ) and dateSelected.date != appointment.date:
        for set in startTimesSet:
            datetime_str = datetime.datetime.strptime (set[0], format)
            # only add the times that are logically possible.
            # ex. don't add 9:00am if it is 12pm in the afternoon

            # though we need to convert the time into 24 hour time format in order to do the comparison.
            # now we only need to do this for the today's date.

            time_in24 = datetime.datetime.strptime (set[0], '%I:%M%p')
            if time_in24.time ( ) < morningUpperBound:
                morningTimeSets.append (set)
            if time_in24.time ( ) < afternoonUpperBound:
                if time_in24.time ( ) > morningUpperBound:
                    afternoonTimeSets.append (set)
            else:
                eveningTimeSets.append (set)

    # now we can process the timeSlot data, if they selected a new date and time.
    if request.method == "POST":
        if "start_time" in request.POST:
            if request.user.is_authenticated:
                myVar = request.POST.get ("start_time")
                # ok we have the start time, now what we need to do is to setup everything to send to confirmation page.
                # really all that we need to pass in is our Appointment object that we are creating.

                # ultimately if the user decides that they would like to alter it, we can  simply delete it.
                # but we wont alter the time slots until after they have confirmed their appointment.

                startTime = datetime.datetime.strptime (myVar, '%I:%M%p')
                endTime = startTime + datetime.timedelta (minutes=appointment.totalDuration)

                print ("So you wish to re-schedule starting at", myVar, " on the date of ", dateSelected.date)
                appointment.start_time = startTime
                appointment.end_time = endTime
                appointment.date = dateSelected.date

                # process the time slot data
                for set in startTimesSet:
                    if set[0] == myVar:
                        for time in set:
                            slot = timeSlot.getTimeSlot (time)
                            setattr (timeSlot, slot, False)

                timeSlot.save ( )
                time_slot.save ( )
                appointment.save ( )

                plaintext = get_template ('Send/re-schedule.txt')
                htmlEmail = get_template ('Send/re-schedule.html')

                content = ({
                    'user': request.user.first_name
                })

                text_content = plaintext.render (content)
                html_content = htmlEmail.render (content)

                msg = EmailMultiAlternatives ("Appointment has been re-scheduled", html_content,
                                              'applenailsalon23@gmail.com',
                                              [request.user.email])

                msg.attach_alternative (html_content, "text/html")
                msg.send ( )

                return redirect ('appointments:confirmation')

    return render (request, "Scheduling/reschedule.html", {'availableDates': workingDays, 'appointment': appointment,
                                                           'morning': morningTimeSets, 'afternoon': afternoonTimeSets,
                                                           'evening': eveningTimeSets, 'date': dateSelected.date})


def deleteAppointment(request, id):
    appointment = Appointment.objects.filter (pk=id).get ( )
    if appointment.technician is not None:
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
        msg = EmailMultiAlternatives ('Appointment has been cancelled!', html_content, 'applenailsalon23@gmail.com',
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
        msg = EmailMultiAlternatives ('Appointment has been cancelled!', html_content, 'applenailsalon23@gmail.com',
                                    [appointment.technician.user.email])
        msg.attach_alternative (html_content, "text/html")

        msg.send ( )

        appointment.delete ( )

        return redirect ('Account:home')
    else:
        
        plaintext = get_template ('Send/userCancellation.txt')
        htmlEmail = get_template ('Send/userCancellation.html')

        content = (
            {'username': request.user.first_name, 'date': appointment.date,
            'technician': 'None' })

        text_content = plaintext.render (content)
        html_content = htmlEmail.render (content)

        # send an e-mail to the technician.
        plaintext = get_template ('Send/technicianCancellation.txt')
        htmlEmail = get_template ('Send/technicianCancellation.html')

        content = (
            {
                'technician': 'None', 'user': request.user.first_name,
                'start_time': appointment.start_time, 'end_time': appointment.end_time, 'date': appointment.date,
            })

        text_content = plaintext.render (content)
        html_content = htmlEmail.render (content)

        appointment.delete ( )

        return redirect ('Account:home')