import django
import os
from datetime import datetime, date
import sys

sys.path.append ("../NailSalon")
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup ( )

from Scheduling.models import timeSlots
from timeslot_process import _Process
from Appointments.models import Sale

_WAIT_QUEUE = []
_WORK_QUEUE = []


def build_fresh_wait_queue(today: date, onday_techs: list): # change to queue of all tech of the day()
    today_date = today
    timeslots = []
    
    for tech in onday_techs:
        timeslots.append(timeSlots.objects.filter(tech=tech, date=today_date).values_list('tech', 'arrive_time')[0])
    print(timeslots)
    
    
    timeslots_list = []
    for ts in timeslots:
        #print(datetime.combine(datetime.today(), ts[1]))
        timeslots_list.append((ts[0], (str)(datetime.combine(datetime.today(), ts[1]))))
    
    sorted_list = sorted(timeslots_list, key=lambda x: x[1])
    for i in sorted_list:
        _WAIT_QUEUE.append(i[0])
        
def build_wait_queue():
    a = Sale.objects.filter(status='working').values_list('technician', 'status')[0]
    print(a)




# Split formatted string data into tuple  "email:priority" -> ("email", priority)
def to_tuple(line:str) -> tuple:
    temp_str = []
    temp_num =  []
    tup = []
    z = 0
    for c in line:
        if (c != ':' and z == 0):
            temp_str.append(c)
        elif (c == "\n"):
            break
        else:
            z = 1
            if (z==1):
                temp_num = c
    
    return ( ((''.join(temp_str)), int(temp_num)) )
# Function to sort the list of tuples by its second item
def Sort_Tuple(lst):
    global _WAIT_QUEUE
    _WAIT_QUEUE = (sorted(lst, key = lambda x: x[1]))



def read_temp():
    f = open("helper/temp1", "r")
    lines = f.readlines()
    f.close()
    read_flag = 0
    wait_tuple_list = []
    for line in lines:
        line = line.replace('\n', '')
        if (line == "_WAIT"):
            pass
        else:
            if line != "_WORK" and read_flag == 0:
                _WAIT_QUEUE.append(to_tuple(line))
            elif line == "_WORK":
                read_flag = 1
            else:
                _WORK_QUEUE.append(to_tuple(line))

def write_temp():
    data = ""
    data += "_WAIT\n"
    for i in _WAIT_QUEUE:
        data += f"{str(i[0])}:{str(i[1])}\n"
    data += "_WORK\n"
    for i in _WORK_QUEUE:
        data += f"{str(i[0])}:{str(i[1])}\n"
    f = open("helper/temp1", "w")
    f.write(data)
    f.close()

def save_queue(queue):
    Sort_Tuple(queue)
    write_temp()

def wait_to_work():
    if len(_WAIT_QUEUE) >=1:
        a = _WAIT_QUEUE.pop(0)
        _WORK_QUEUE.append((a[0], a[1]+1))
        save_queue(_WAIT_QUEUE)
        return len(_WAIT_QUEUE)
    else:
        return 0

def work_to_wait(email):
    if len(_WORK_QUEUE) >=1:
        for i in _WORK_QUEUE:
            if i[0] == email:
                a = _WORK_QUEUE.remove(i)
                _WAIT_QUEUE.append(i)
        save_queue(_WAIT_QUEUE)
        return len(_WAIT_QUEUE)
    else:
        return 0






def main():
    global _WAIT_QUEUE
    read_temp()
    
    wait_to_work()
    work_to_wait('c@email.com')



'''
Khoa's stuff:
    process = _Process(date(2022, 11, 12))
    
    onday_techs = []
    for tech in process._get_time_scheduled_techs():
        onday_techs.append(tech[0])
        
    #build_fresh_wait_queue(date(2022, 11, 12), onday_techs)
    #print(_WAIT_QUEUE)
    build_wait_queue()
    '''
    
if __name__ == '__main__':
    main()