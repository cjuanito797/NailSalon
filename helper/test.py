import datetime
import django
import os
import calendar
import sys

sys.path.append ("../NailSalon")
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup ( )

from Account.models import User

a = [
    User (email='a@a.com', first_name='a', last_name='aa', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='b@a.com', first_name='a', last_name='aa', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='c@a.com', first_name='a', last_name='aa', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='d@a.com', first_name='a', last_name='aa', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='e@a.com', first_name='a', last_name='aa', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='f@a.com', first_name='a', last_name='aa', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='g@a.com', first_name='a', last_name='aa', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='h@a.com', first_name='a', last_name='aa', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='i@a.com', first_name='a', last_name='aa', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='j@a.com', first_name='a', last_name='aa', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' ')
]
for i in a:
    i.save ( )

print ("User done!")
# DELETE FROM Account_user;
# DELETE FROM sqlite_sequence where name = 'Account_user';


from Account.models import Customer

a = [
    Customer (user_id=1, bio=''),
    Customer (user_id=2, bio=''),
    Customer (user_id=3, bio=''),
    Customer (user_id=4, bio=''),
    Customer (user_id=5, bio=''),

]
for i in a:
    i.save ( )
print ("Customer done!")
# DELETE FROM Account_customer;

from Scheduling.models import TechnicianSchedule

a = [
    TechnicianSchedule (
        tech="f@a.com",
        monday_availability=True,
        monday_timeIn=datetime.time (9, 0),
        monday_timeOut=datetime.time (17, 0),
        tuesday_availability=True,
        tuesday_time_In=datetime.time (9, 0),
        tuesday_time_Out=datetime.time (17, 0),
        wednesday_availability=True,
        wednesday_time_In=datetime.time (9, 0),
        wednesday_time_Out=datetime.time (17, 0),
        thursday_availability=True,
        thursday_time_In=datetime.time (9, 0),
        thursday_time_Out=datetime.time (17, 0),
        friday_availability=True,
        friday_time_In=datetime.time (9, 0),
        friday_time_Out=datetime.time (17, 0),
        saturday_availability=True,
        saturday_time_In=datetime.time (9, 0),
        saturday_time_Out=datetime.time (17, 0),
        sunday_availability=True,
        sunday_time_In=datetime.time (9, 0),
        sunday_time_Out=datetime.time (17, 0),
    ),
    TechnicianSchedule (
        tech="g@a.com",
        monday_availability=True,
        monday_timeIn=datetime.time (9, 0),
        monday_timeOut=datetime.time (17, 0),
        tuesday_availability=True,
        tuesday_time_In=datetime.time (9, 0),
        tuesday_time_Out=datetime.time (17, 0),
        wednesday_availability=True,
        wednesday_time_In=datetime.time (9, 0),
        wednesday_time_Out=datetime.time (17, 0),
        thursday_availability=True,
        thursday_time_In=datetime.time (9, 0),
        thursday_time_Out=datetime.time (17, 0),
        friday_availability=True,
        friday_time_In=datetime.time (9, 0),
        friday_time_Out=datetime.time (17, 0),
        saturday_availability=True,
        saturday_time_In=datetime.time (9, 0),
        saturday_time_Out=datetime.time (17, 0),
        sunday_availability=True,
        sunday_time_In=datetime.time (9, 0),
        sunday_time_Out=datetime.time (17, 0),
    ),
    TechnicianSchedule (
        tech="h@a.com",
        monday_availability=True,
        monday_timeIn=datetime.time (9, 0),
        monday_timeOut=datetime.time (17, 0),
        tuesday_availability=True,
        tuesday_time_In=datetime.time (9, 0),
        tuesday_time_Out=datetime.time (17, 0),
        wednesday_availability=True,
        wednesday_time_In=datetime.time (9, 0),
        wednesday_time_Out=datetime.time (17, 0),
        thursday_availability=True,
        thursday_time_In=datetime.time (9, 0),
        thursday_time_Out=datetime.time (17, 0),
        friday_availability=True,
        friday_time_In=datetime.time (9, 0),
        friday_time_Out=datetime.time (17, 0),
        saturday_availability=True,
        saturday_time_In=datetime.time (9, 0),
        saturday_time_Out=datetime.time (17, 0),
        sunday_availability=True,
        sunday_time_In=datetime.time (9, 0),
        sunday_time_Out=datetime.time (17, 0),
    ),
    TechnicianSchedule (
        tech="i@a.com",
        monday_availability=True,
        monday_timeIn=datetime.time (9, 0),
        monday_timeOut=datetime.time (17, 0),
        tuesday_availability=True,
        tuesday_time_In=datetime.time (9, 0),
        tuesday_time_Out=datetime.time (17, 0),
        wednesday_availability=True,
        wednesday_time_In=datetime.time (9, 0),
        wednesday_time_Out=datetime.time (17, 0),
        thursday_availability=True,
        thursday_time_In=datetime.time (9, 0),
        thursday_time_Out=datetime.time (17, 0),
        friday_availability=True,
        friday_time_In=datetime.time (9, 0),
        friday_time_Out=datetime.time (17, 0),
        saturday_availability=True,
        saturday_time_In=datetime.time (9, 0),
        saturday_time_Out=datetime.time (17, 0),
        sunday_availability=True,
        sunday_time_In=datetime.time (9, 0),
        sunday_time_Out=datetime.time (17, 0),
    ),
    TechnicianSchedule (
        tech="j@a.com",
        monday_availability=True,
        monday_timeIn=datetime.time (9, 0),
        monday_timeOut=datetime.time (17, 0),
        tuesday_availability=True,
        tuesday_time_In=datetime.time (9, 0),
        tuesday_time_Out=datetime.time (17, 0),
        wednesday_availability=True,
        wednesday_time_In=datetime.time (9, 0),
        wednesday_time_Out=datetime.time (17, 0),
        thursday_availability=True,
        thursday_time_In=datetime.time (9, 0),
        thursday_time_Out=datetime.time (17, 0),
        friday_availability=True,
        friday_time_In=datetime.time (9, 0),
        friday_time_Out=datetime.time (17, 0),
        saturday_availability=True,
        saturday_time_In=datetime.time (9, 0),
        saturday_time_Out=datetime.time (17, 0),
        sunday_availability=True,
        sunday_time_In=datetime.time (9, 0),
        sunday_time_Out=datetime.time (17, 0),
    ),

]
for i in a:
    i.save ( )
print ("Tech_Schedule done!")

from Account.models import Technician

a = [
    Technician(user_id=6, bio='', schedule_id=1, profilePicture='technicians/2022/10/04/images.jpeg'),
    Technician(user_id=7, bio='', schedule_id=2, profilePicture=' '),
    Technician(user_id=8, bio='', schedule_id=3, profilePicture=' '),
    Technician(user_id=9, bio='', schedule_id=4, profilePicture=' '),
    Technician(user_id=10, bio='', schedule_id=5, profilePicture=' '), 
    # Technician(user_id=6, bio='', schedule_id=1),
    # Technician(user_id=7, bio='', schedule_id=2),
    # Technician(user_id=8, bio='', schedule_id=3),
    # Technician(user_id=9, bio='', schedule_id=4),
    # Technician(user_id=10, bio='', schedule_id=5),
]
for i in a:
    i.save ( )
print ("Technician done!")
# DELETE FROM Account_technician;


from Appointments.models import Category

a = [
    Category (name='Wax', slug='wax'),
    Category (name='Manicure', slug='manicure'),
    Category (name='Pedicure', slug='pedicure')
]
for i in a:
    i.save ( )
print ("Category done!")
# DELETE FROM Appointments_category;


from Appointments.models import Service

b = datetime.timedelta (minutes=15)
c = datetime.timedelta (minutes=30)
d = datetime.timedelta (minutes=45)
e = datetime.timedelta (minutes=60)
f = datetime.timedelta (minutes=75)

a = [
    Service (category_id=2, name='Acrylic Full Set', description='...', slug='acrylic-full-set', price=37, duration=d,
             image=''),
    Service (category_id=2, name='Acrylic Full Set with Shellac', description='...',
             slug='acrylic-full-set-with-shellac', price=50, duration=f, image=''),
    Service (category_id=2, name='Acrylic Full Set White Tips', description='...', slug='acrylic-full-set-white-tips',
             price=42, duration=e, image=''),
    Service (category_id=2, name='Acrylic Fill In', description='...', slug='acrylic-fill-in', price=27, duration=c,
             image=''),
    Service (category_id=2, name='Acrylic Fill In with Shellac', description='...', slug='acrylic-fill-in-with-shellac',
             price=40, duration=e, image=''),
    Service (category_id=2, name='Ombre Full Set', description='...', slug='ombre-full-set', price=55, duration=f,
             image=''),
    Service (category_id=2, name='Ombre refill', description='...', slug='ombre-refill', price=40, duration=d,
             image=''),
    Service (category_id=2, name='Ombre Pink refill', description='...', slug='ombre-pink-refill', price=30, duration=b,
             image=''),
    Service (category_id=2, name='Pink and White Full Set', description='...', slug='pink-and-white-full-set', price=55,
             duration=f, image=''),
    Service (category_id=2, name='Pink and White refill', description='...', slug='pink-and-white-refill', price=45,
             duration=e, image=''),
    Service (category_id=2, name='Pink refill', description='...', slug='pink-refill', price=30, duration=c, image=''),
    Service (category_id=2, name='Dip Powder with Manicure', description='...', slug='dip-powder-with-manicure',
             price=45, duration=d, image=''),
    Service (category_id=2, name='Dip Powder Full Set', description='...', slug='dip-powder-full-set', price=50,
             duration=d, image=''),
    Service (category_id=2, name='Dip Powder refill', description='...', slug='dip-powder-refill', price=30, duration=c,
             image=''),
    Service (category_id=3, name='Luxury Spa Pedicure', description='...', slug='luxury-spa-pedicure', price=50,
             duration=e, image=''),
    Service (category_id=3, name='Luxury Spa Pedicure with Shellac', description='...',
             slug='luxury-spa-pedicure-with-shellac', price=65, duration=f, image=''),
    Service (category_id=3, name='Luxury Spa Pedicure and Manicure', description='...',
             slug='luxury-spa-pedicure-and-manicure', price=70, duration=f, image=''),
    Service (category_id=3, name='Deluxe Spa Pedicure', description='...', slug='deluxe-spa-pedicure', price=42,
             duration=d, image=''),
    Service (category_id=3, name='Deluxe Spa Pedicure with Shellac', description='...',
             slug='deluxe-spa-pedicure-with-shellac', price=57, duration=e, image=''),
    Service (category_id=3, name='Deluxe Spa Pedicure and Manicure', description='...',
             slug='deluxe-spa-pedicure-and-manicure', price=62, duration=f, image=''),
    Service (category_id=3, name='Smoothie Spa Pedicure', description='...', slug='smoothie-spa-pedicure', price=32,
             duration=c, image=''),
    Service (category_id=3, name='Smoothie Spa Pedicure with Shellac', description='...',
             slug='smoothie-spa-pedicure-with-shellac', price=47, duration=c, image=''),
    Service (category_id=3, name='Smoothie Spa Pedicure and Manicure', description='...',
             slug='smoothie-spa-pedicure-and-manicure', price=52, duration=d, image=''),
    Service (category_id=1, name='Wax Eyebrow', description='...', slug='wax-eyebrow', price=13, duration=b, image=''),
    Service (category_id=1, name='Wax Upper Lip', description='...', slug='wax-upper-lip', price=6, duration=b,
             image=''),
    Service (category_id=1, name='Wax Chin and Upper Lip', description='...', slug='wax-chin-and-upper-lip', price=10,
             duration=b, image=''),
    Service (category_id=1, name='Wax Sideburns', description='...', slug='wax-sideburn', price=18, duration=b,
             image=''),
    Service (category_id=1, name='Wax Upper and Lower Lip', description='...', slug='wax-upper-and-lower-lip', price=10,
             duration=b, image=''),
    Service (category_id=1, name='Wax Full Facw', description='...', slug='wax-full-face', price=42, duration=d,
             image=''),
    Service (category_id=1, name='Wax Under Arm', description='...', slug='wax-under-arm', price=22, duration=c,
             image=''),
    Service (category_id=1, name='Wax Half Arm', description='...', slug='wax-half-arm', price=30, duration=c,
             image=''),
    Service (category_id=1, name='Wax Full Arm', description='...', slug='wax-full-arm', price=60, duration=e,
             image=''),
    Service (category_id=1, name='Wax Half Leg', description='...', slug='wax-half-leg', price=40, duration=c,
             image=''),
    Service (category_id=1, name='Wax Full Leg', description='...', slug='wax-full-leg', price=80, duration=e,
             image=''),
    Service (category_id=1, name='Wax Back', description='...', slug='wax-back', price=50, duration=c, image=''),

]
for i in a:
    i.save ( )
print ("Service done!")
# DELETE FROM Appointments_service;

from Appointments.models import Appointment

g = datetime.time (10, 30, 00)
h = datetime.time (11, 00, 00)
i = datetime.time (11, 30, 00)
j = datetime.time (11, 45, 00)
k = datetime.time (12, 00, 00)
l = datetime.date (2022, 10, 10)
m = datetime.date (2022, 10, 11)
n = datetime.date (2022, 10, 12)
a = [
    Appointment (customer_id=1, totalDuration=60, date=l, end_time=i, start_time=g, totalCharge=50),
    Appointment (customer_id=2, totalDuration=60, date=l, end_time=i, start_time=g, totalCharge=50),
    Appointment (customer_id=3, totalDuration=30, date=l, end_time=k, start_time=i, totalCharge=50),
    Appointment (customer_id=4, totalDuration=30, date=m, end_time=k, start_time=i, totalCharge=50),
    Appointment (customer_id=5, totalDuration=30, date=m, end_time=h, start_time=g, totalCharge=50),
    Appointment (customer_id=1, totalDuration=60, date=m, end_time=i, start_time=g, totalCharge=50),
    Appointment (customer_id=2, totalDuration=60, date=n, end_time=k, start_time=h, totalCharge=50),
]
for i in a:
    i.save ( )
print ("Appointment done!")
# DELETE FROM Appointments_appointment;
