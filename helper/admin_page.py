import django
import os
from datetime import datetime, date
import sys

sys.path.append ("../NailSalon")
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup ( )

from Appointments.models import Sale

class Admin():
    def __init__():
        pass
    
    def change_tech(**kargs): 
        if len(kargs) == 2:      # change technicians for each sale (sale id, new tech)
            pass
        elif len(kargs) == 2:    #
            pass
        
    

