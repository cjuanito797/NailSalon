
import datetime
import django
import os
import calendar
import sys

sys.path.append("../NailSalon")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup()
'''
from Appointments.models import Category
a = [
    Category(name='Manicure',slug='manicure'), 
    Category(name='Pedicure',slug='pedicure'),
    Category(name='Wax',slug='wax'),
]
for i in a:
    i.save()
#DELETE FROM Appointments_category;


from Appointments.models import Service
b = datetime.timedelta(minutes = 30)
c = datetime.timedelta(minutes = 45)
d = datetime.timedelta(minutes = 15)
e = datetime.timedelta(minutes = 60)

a = [
    Service(category_id=2, name='Classic Manicure', description='...', slug='classic-manicure', price=35, duration=b, image=''),
    Service(category_id=3, name='Classic Pedicure', description='...', slug='Classic-pedicure', price=25, duration=c, image=''),
    Service(category_id=2, name='Full Set', description='...', slug='full-set', price=65, duration=e, image=''),
    Service(category_id=2, name='Tropical Manicure', description='...', slug='tropical-manicure', price=35, duration=d, image='')
]
for i in a:
    i.save()
#DELETE FROM Appointments_service;

from Appointments.models import Appointment
b = datetime.time(10,30,00)
b1 = datetime.time(11,00,00)
c = datetime.time(11,30,00)
d = datetime.time(11,45,00)
e = datetime.time(12,00,00)
f = datetime.date(2022,9,10)
f1 = datetime.date(2022,9,12)
#g = datetime.timedelta(minutes = 60)
a = [
    Appointment(customer_id=2, totalDuration=60, date =f, end_time=c, start_time=b,totalCharge=50),
    Appointment(customer_id=1, totalDuration=30, date =f1, end_time=c, start_time=b1,totalCharge=50),
    Appointment(customer_id=3, totalDuration=30, date =f, end_time=c, start_time=b1,totalCharge=50),
    Appointment(customer_id=8, totalDuration=45, date =f1, end_time=d, start_time=b1,totalCharge=50),
    Appointment(customer_id=9, totalDuration=30, date =f, end_time=c, start_time=b1,totalCharge=50),
    Appointment(customer_id=10, totalDuration=90, date =f1, end_time=e, start_time=b,totalCharge=50),
]
for i in a:
    i.save()
#DELETE FROM Appointments_appointment;
'''

from Account.models import Customer
a = [
    Customer(user_id=1, bio=''),
    Customer(user_id=2, bio=''),
    Customer(user_id=3, bio=''),
    Customer(user_id=4, bio=''),
    Customer(user_id=5, bio=''), 

]
for i in a:
    i.save()
#DELETE FROM Account_customer;



from Account.models import Technician
a = [
    Technician(user_id=6, bio=''),
    Technician(user_id=7, bio=''),
    Technician(user_id=8, bio=''),
    Technician(user_id=9, bio=''),
    Technician(user_id=10, bio=''), 

]
for i in a:
    i.save()
#DELETE FROM Account_customer;


'''
from Account.models import User
a = [
    User(email='a@a.com', first_name='a', last_name='aa', street_num=' ', state=' ', zipcode=' ', city=' ', phoneNumber='000', bio =' '),
    User(email='b@a.com', first_name='a', last_name='aa', street_num=' ', state=' ', zipcode=' ', city=' ', phoneNumber='000', bio =' '),
    User(email='c@a.com', first_name='a', last_name='aa', street_num=' ', state=' ', zipcode=' ', city=' ', phoneNumber='000', bio =' '),
    User(email='d@a.com', first_name='a', last_name='aa', street_num=' ', state=' ', zipcode=' ', city=' ', phoneNumber='000', bio =' '),
    User(email='e@a.com', first_name='a', last_name='aa', street_num=' ', state=' ', zipcode=' ', city=' ', phoneNumber='000', bio =' '),
    User(email='f@a.com', first_name='a', last_name='aa', street_num=' ', state=' ', zipcode=' ', city=' ', phoneNumber='000', bio =' '),
    User(email='g@a.com', first_name='a', last_name='aa', street_num=' ', state=' ', zipcode=' ', city=' ', phoneNumber='000', bio =' '),
    User(email='h@a.com', first_name='a', last_name='aa', street_num=' ', state=' ', zipcode=' ', city=' ', phoneNumber='000', bio =' '),
    User(email='i@a.com', first_name='a', last_name='aa', street_num=' ', state=' ', zipcode=' ', city=' ', phoneNumber='000', bio =' '),
]
for i in a:
    i.save()
#DELETE FROM Account_user;
#DELETE FROM sqlite_sequence where name = 'Account_user';
'''