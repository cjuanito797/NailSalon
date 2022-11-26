import datetime
import django
import os
import calendar
import sys
from datetime import date
import calendar
sys.path.append ("../NailSalon")
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup ( )

cc = ["f@a.com", "g@a.com", "h@a.com","i@a.com", "j@a.com", "k@a.com", "l@a.com", "m@a.com", "n@a.com", "o@a.com", "p@a.com"]
def get_date():

    bb=[]
    for i in range(30):
        a = (date.today() + datetime.timedelta(days=i))
        #c = a.strftime("%Y,%m,%d")
        b = calendar.day_name[a.weekday()]
        if b != 'Sunday':
            aa.append(a)
        else:
            bb.append(a)
    return [aa,bb]

'''
from Account.models import User

a = [
    User (email='a@a.com', first_name='Duy', last_name='Ha', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='b@a.com', first_name='Khoa', last_name='Tran', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='c@a.com', first_name='Brazan', last_name='Gonzales', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='d@a.com', first_name='Nick', last_name='Wroblewski', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='e@a.com', first_name='Juan', last_name='Lizarraga', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='f@a.com', first_name='Tan', last_name='Pham', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='g@a.com', first_name='My', last_name='Nguyen', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='h@a.com', first_name='Minh', last_name='Phan', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='i@a.com', first_name='Nam', last_name='Dang', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='k@a.com', first_name='Tu', last_name='Luong', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '
    User (email='l@a.com', first_name='Vu', last_name='Ho', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='m@a.com', first_name='Jenny', last_name='Tran', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='n@a.com', first_name='Teresa', last_name='Do', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='o@a.com', first_name='Nhi', last_name='Phan', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='p@a.com', first_name='Van', last_name='Vo', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
          phoneNumber='000', bio=' '),
    User (email='j@a.com', first_name='Yen', last_name='Nguyen', street_num=' ', state='Nebraska', zipcode=' ', city=' ',
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

for i in cc:
    TechnicianSchedule (tech=i,
        monday_availability=True,
        monday_time_In=datetime.time (9, 0),
        monday_time_Out=datetime.time (17, 0),
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
        sunday_availability=False,
        sunday_time_In=datetime.time (0, 0),
        sunday_time_Out=datime.time (0, 0)).save()a

print ("Tech_Schedule done!")

from Account.models import Technician

a = [
    Technician(user_id=6, bio='', schedule_id=1, profilePicture='technicians/2022/10/05/11.jpg'),
    Technician(user_id=7, bio='', schedule_id=2, profilePicture='technicians/2022/10/05/1.jpg'),
    Technician(user_id=8, bio='', schedule_id=3, profilePicture='technicians/2022/10/05/2.jpg'),
    Technician(user_id=9, bio='', schedule_id=4, profilePicture='technicians/2022/10/05/3.jpg'),
    Technician(user_id=10, bio='', schedule_id=5, profilePicture='technicians/2022/10/05/4.jpg'), 
    Technician(user_id=11, bio='', schedule_id=6, profilePicture='technicians/2022/10/05/5.jpg'), 
    Technician(user_id=12, bio='', schedule_id=7, profilePicture='technicians/2022/10/05/6.jpg'), 
    Technician(user_id=13, bio='', schedule_id=8, profilePicture='technicians/2022/10/05/7.jpg'), 
    Technician(user_id=14, bio='', schedule_id=9, profilePicture='technicians/2022/10/05/8.jpg'), 
    Technician(user_id=15, bio='', schedule_id=10, profilePicture='technicians/2022/10/05/9.jpg'), 
    Technician(user_id=16, bio='', schedule_id=11, profilePicture='technicians/2022/10/05/10.jpg'),
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
'''


from Appointments.models import Appointment

a = datetime.time (10, 30, 00)
b = datetime.time (11, 30, 00)
aa = get_date()[0]

for z in aa:
    for id in range(1,6):
        Appointment (customer_id=id, totalDuration=60, date=z, end_time=b, start_time=a, totalCharge=50).save()

print ("Appointment done!")
# DELETE FROM Appointments_appointment;


from Scheduling.models import timeSlots
aa = get_date()

for i in aa[0]:
    for email in cc:
        timeSlots (tech=email, date=i, arrive_time =None, nine_00_am = True, nine_15am = True, nine_30am = True, nine_45am = True,
        ten_00_am = True, ten_15am = True, ten_30am = True, ten_45am = True, eleven_00_am = True, eleven_15am = True, eleven_30am = True,
        eleven_45am = True, twelve_00_pm = True, twelve_15pm = True, twelve_30pm = True, twelve_45pm = True, one_00_pm = True,
        one_15pm = True, one_30pm = True, one_45pm = True, two_00_pm = True, two_15pm = True, two_30pm = True, two_45pm = True,
        three_00_pm = True, three_15pm = True, three_30pm = True, three_45pm = True, four_00_pm = True, four_15pm = True, four_30pm = True,
        four_45pm = True).save ( )
for i in aa[1]:
    for email in cc:
        timeSlots (tech=email, date=i, arrive_time =None).save ( )
print ("Timeslot done!")



from Calendar.models import calendarEntry
from Account.models import Technician
aa = get_date()[0]
tech_id = [6,7,8,9,10,11,12,13,14,15,16]

for i in aa:
    d = calendarEntry(date=i)
    d.save()
    for id in tech_id:
        d.technicians.add(Technician.objects.get(user_id=id))
        d.save()
print("Calendar entry done!")


'''
from Account.models import Technician
from Appointments.models import Sale, Appointment, Service
import random

b = [Sale(appointment_id=1, service_id=5, technician_id=8),
    Sale(appointment_id=2, service_id=6, technician_id=1),
    Sale(appointment_id=3, service_id=11, technician_id=2),
    Sale(appointment_id=4, service_id=14, technician_id=3),
    Sale(appointment_id=5, service_id=13, technician_id=4),
    Sale(appointment_id=6, service_id=22, technician_id=5),
    Sale(appointment_id=7, service_id=9, technician_id=6),    
]
for i in b:
    i.save()
print("Sale done!")

for j in range(1,8):
    a = Appointment.objects.get(id=random.randint(1,135))
    a.services.add(Service.objects.get(id=random.randint(1,20)))
    a.save()
print("Insert done!")
'''




