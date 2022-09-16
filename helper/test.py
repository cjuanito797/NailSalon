
import datetime
import django
import os
import calendar
import sys

sys.path.append("../NailSalon")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup()

from Appointments.models import Service


d = datetime.timedelta(minutes = 30)
a = Service(category_id=1, name='Manicure', description='3', slug='4', price=35, duration=d, image='')
a.save()



