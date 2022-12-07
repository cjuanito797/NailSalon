import django
import os
import datetime
#from datetime import date
import sys
import math

sys.path.append ("../NailSalon")
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup ( )
from Appointments.models import Appointment

FILE_DIR = "helper/appointment_queue"
_COUNTED_APPOINTMENT = []


#CONTROL FUNCTIONS----------------------------------------------
def get_next_frame_available(current_date: datetime.date):
    global _COUNTED_APPOINTMENT
    _read_data()
    
    # Query only appointments id that not set in the file, and set flag to resolve later
    if str(current_date) in _COUNTED_APPOINTMENT:
        flag_exist = True
        temp = list(Appointment.objects.filter(date=current_date, status='active')
                    .exclude(id__in=_COUNTED_APPOINTMENT[str(current_date)])
                    .values('id', 'end_time'))
    else:
        flag_exist = False
        temp = list(Appointment.objects.filter(date=current_date, status='active')
                    .values('id', 'end_time'))
    
    # Set end_time datatype fit to sort
    endtime_list = []
    for t in temp:
        if t['end_time'] != None:
            t['end_time'] = datetime.datetime.combine(datetime.datetime.min, t['end_time']) - datetime.datetime.min
        endtime_list.append(t)
    print(endtime_list)
    # Sort and reset end_time datatype
    next_finish = sorted(endtime_list, key=lambda x: x['end_time'])[0]
    next_finish['end_time'] = (datetime.datetime.min + next_finish['end_time']).time()
    # Calculate next time available
    next_slot = math.floor((next_finish['end_time'].minute + 15)/15)
    if next_slot > 4:
        next_finish['end_time'] = datetime.time(next_finish['end_time'].hour + 1, 0, 0)
    else:
        next_finish['end_time'] = datetime.time(next_finish['end_time'].hour, next_slot * 15, 0)

    print(next_finish['end_time'])
    # Continue to resolve if id that not set in the file or not
    # if id already set in the file, add id into that date list
    if flag_exist == True:
        _COUNTED_APPOINTMENT[str(current_date)].append(next_finish['id'])
    # if not in the file, create new date key and add id into key
    else:
        _COUNTED_APPOINTMENT[str(current_date)] = [next_finish['id'],]
        
    #_write_data()
    return next_finish['end_time']
        
def newday_clean_up(filedir=FILE_DIR):
    global _COUNTED_APPOINTMENT
    _read_data(filedir)
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
    if yesterday in _COUNTED_APPOINTMENT:
        del _COUNTED_APPOINTMENT[yesterday]
    _write_data(filedir)

#BASIC FUNCTIONS-----------------------------------------------------------
def _write_data(filedir=FILE_DIR):
    data = ""
    for key in _COUNTED_APPOINTMENT:
        data += f"_{key}\n"
        for value in _COUNTED_APPOINTMENT[key]:
            data += f"{value}\n"
    f = open(filedir, "w")
    f.write(data)
    f.close()

def _read_data(filedir=FILE_DIR):
    global _COUNTED_APPOINTMENT
    
    if os.stat("helper/appointment_queue").st_size != 0:
        f = open("helper/appointment_queue", "r")
        lines = f.readlines()
        f.close()
        
        _COUNTED_APPOINTMENT = {}
        
        read_flag = 0
        temp = None
        for line in lines:
            if "_" in line:
                line = line[1:]
                line = line[:-1]
                #date_obj = datetime.strptime(line, "%Y-%m-%d").date()
                temp = line
                _COUNTED_APPOINTMENT[line] = []
            else:
                line = line[:-1]
                _COUNTED_APPOINTMENT[temp].append(line)
    else:
        _COUNTED_APPOINTMENT = {}


