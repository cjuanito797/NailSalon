from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from datetime import date
import calendar
from django.urls import reverse
from django.views.generic import FormView
from django.http import HttpResponse
from .forms import RegistrationForm, LoginForm, EmailChangeForm
from .models import Technician, User, Customer
from django.contrib.auth import logout
from django.template import loader
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .forms import EditAddress, messageForm
from Appointments.models import Appointment, Sale
from Scheduling.models import TechnicianSchedule
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if (request.session.get ('is_signedIn'), True):
            if str(request.user) != 'test@email.com':
                user_obj=User.objects.get(email=str(request.user))
                if (user_obj.isTechnician==False and user_obj.is_staff == False):
                    return redirect('account:customerView')
                elif(user_obj.is_staff):
                    return redirect('manager:home')
                else:
                    return redirect('account:technicianView')
                
            else:
                return redirect ('manager/')
        else:
            print ("User is not logged in!")
    else:
        return render (request, "base.html")


def availableTechs(request):
    # print all available technicians for that day.
    curr_date = date.today ( )
    dayOfWeek = calendar.day_name[curr_date.weekday ( )]

    if dayOfWeek == 'Monday':
        techs = Technician.objects.filter (schedule__monday_availability=True)

    elif dayOfWeek == 'Tuesday':
        techs = Technician.objects.filter (schedule__tuesday_availability=True)

    elif dayOfWeek == 'Wednesday':
        techs = Technician.objects.filter (schedule__wednesday_availability=True)

    elif dayOfWeek == 'Thursday':
        techs = Technician.objects.filter (schedule__thursday_availability=True)

    elif dayOfWeek == 'Friday':
        techs = Technician.objects.filter (schedule__friday_availability=True)

    elif dayOfWeek == 'Saturday':
        techs = Technician.objects.filter (schedule__saturday_availability=True)

    else:
        techs = Technician.objects.filter (schedule__sunday_availability=True)

    return render (request, "availableTechs.html", {"techs": techs, "dayOfWeek": dayOfWeek})


@cache_control (no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    form = LoginForm (request.POST)
    if form.is_valid ( ):

        cd = form.cleaned_data
        user = authenticate (request,
                             username=cd['email'],
                             password=cd['password'])
        request.session['is_signedIn'] = True

        # here we should redirect a user to seperate views depending on whether they are a customer, tech or admin.
        if user is not None:
            if user.is_active:
                
                login (request, user)
                return render  ('account:customerView')
            else:
                return HttpResponse ('Disabled Account')
        else:
            return HttpResponse ('Invalid Login')
    else:
        form = LoginForm ( )
    return render (request, 'registration/login.html', {'form': form})

@login_required (login_url='/login/')
def technicianView(request):
    if request.user.is_authenticated:

        # get all of the appointments pertaining to this user.
        # get the id of the currently signed in technician
        tech = Technician.objects.filter(user__email=request.user.email).get()

        my_appointments = Appointment.objects.filter(status__exact='active', technician_id=tech.id)

        if request.method == 'POST':
            if "Send" in request.POST:
                my_id = request.POST.get('Send')
                new_message = messageForm(request.POST)
                print(new_message.errors)
                if new_message.is_valid():
                    subject = new_message['subject'].value()
                    message = new_message['message'].value()

                    appointment = Appointment.objects.filter(pk=my_id).get()

                    # prepare to send e-mail to customer.
                    plaintext = get_template('Send/contactCustomer.txt')
                    htmlEmail = get_template('Send/contactCustomer.html')

                    content = {
                        'customer': appointment.customer.first_name, 'subject': subject,
                        'message': message, 'technicianEmail': request.user.email
                    }

                    text_content = plaintext.render(content)
                    html_content = htmlEmail.render(content)

                    msg = EmailMultiAlternatives ('Question regarding your appointment', html_content,
                                                  'applenailsalon23@gmail.com',
                                                  [appointment.customer.email])
                    msg.attach_alternative (html_content, "text/html")
                    msg.send ( )

                    return redirect('account:home')

        else:
            message = messageForm()

        return render (request, "account/technicianView.html",
                           {'my_appointments': my_appointments, 'message_form': messageForm})



def gallery(request):
    return render (request, 'Home/gallery.html')


def services(request):
    return render (request, 'Home/services.html')


def aboutUs(request):
    return render (request, 'Home/aboutUs.html')


@never_cache
@cache_control (no_cache=True, must_revalidate=True, no_store=True)
@login_required (login_url='/login/')
def profile(request):
    if request.user.is_authenticated:
        if (request.session.get ('is_signedIn'), True):
            username = request.user.email
            this_user = User.objects.get (pk=request.user.id)
            template = loader.get_template ('account/profile.html')

            context = {
                'this_user': this_user
            }

            return HttpResponse (template.render (context, request))
        else:
            print ("User is not signed in!")
            return redirect ('account:home')
    else:
        return redirect ('account:home')


@login_required (login_url='/login/')
def securitySettings(request):
    return render (request, "account/securitySettings.html")


@login_required (login_url='/login/')
def changePassword(request):
    if request.user.is_authenticated:
        form = PasswordChangeForm (request.user, request.POST)

        if form.is_valid ( ):
            user = form.save (commit=False)
            form.save ( )
            update_session_auth_hash (request, user)

            return redirect ('account:user_login')
        return render (request, 'account/changePassword.html', {'form': form})

    def get(self, request):
        form = PasswordChangeForm ( )
        return render (request, 'account/changePassword.html', {'form': form})


@login_required (login_url='/login/')
def changeEmail(request):
    if request.user.is_authenticated:
        form = EmailChangeForm (request.user, request.POST)

        if form.is_valid ( ):
            user = form.save (commit=False)
            form.save ( )
            update_session_auth_hash (request, user)

            return redirect ('account:user_login')
        return render (request, 'account/changeEmail.html', {'form': form})

    def get(self, request):
        form = EmailChangeForm ( )
        return render (request, 'account/changeEmail.html', {'form': form})


@login_required (login_url='/login/')
def deleteAccount(request):
    this_user = User.objects.get (pk=request.user.id)
    this_user.delete ( )
    return render (request, "account/deleteAccount.html")


@never_cache
@cache_control (no_cache=True, must_revalidate=True, no_store=True)
@login_required (login_url='/login/')
def logout(request):
    if request.user.is_authenticated:
        request.session['is_signedIn'] = False
        logout (request)
        del request.session['is_signedIn']
        request.session.flush ( )
        return HttpResponseRedirect ("/")


@never_cache
@cache_control (no_cache=True, must_revalidate=True, no_store=True)
@login_required (login_url='/login/')
def customerView(request):
    if request.user.is_authenticated:
        if (request.session.get ('is_signedIn'), True):
            username = request.user.email
            this_user = User.objects.get (pk=request.user.id)
            # get the future appointments pertaining to the user.
            my_appointments = Appointment.objects.filter (customer_id=this_user.id, status__exact='active').all ( )
            apptCount = my_appointments.count ( )

            # build a query set for all of the sale items in the customers upcoming appointments
            saleItems = []
            for x in my_appointments:
                # get a query set of sale items, for each  appointment.
                sales = Sale.objects.filter (appointment_id=x.id).all ( )
                for sale in sales:
                    saleItems.append (sale)

            return render (request, "account/customerView.html",
                           {'this_user': this_user, 'my_appointments': my_appointments, 'apptCount': apptCount,
                            'sale_items': saleItems})
        else:
            print ("User is not signed in!")
            return redirect ('account:home')
    else:
        return redirect ('account:home')


class registration_view (FormView):
    def post(self, request):
        form = RegistrationForm (request.POST)

        if form.is_valid ( ):
            # create a customer object and attatch it to the newly created user
            new_user = form.save (commit=False)
            form.save ( )

            new_customer = Customer.objects.create (user=new_user, bio='blank')
            new_customer.save ( )

            return redirect (reverse ('account:user_login'))
        return render (request, 'registration/registration.html', {'form': form})

    def get(self, request):
        form = RegistrationForm ( )
        return render (request, 'registration/registration.html', {'form': form})


@login_required
def edit_address(request):
    if request.method == "POST":
        form = EditAddress (request.POST or None, instance=request.user, use_required_attribute=False)
        if form.is_valid ( ):
            form.save ( )
            return render (request, 'account/editAddress.html')

    else:
        form = EditAddress (request.POST or None, instance=request.user, use_required_attribute=False)
    return render (request, 'account/editAddress.html', {'form': form})

# Begin to add all of the CRUD operations on the Account Side

@login_required
def techSchedule(request):
    return render (request, "account/techSchedule.html")