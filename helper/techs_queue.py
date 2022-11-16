import django
import os
from datetime import datetime, date
import sys

sys.path.append ("../NailSalon")
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'NailSalon.settings')
django.setup ( )

from Scheduling.models import timeSlots
from Appointments.models import Sale

_WAIT_QUEUE = []
_WORK_QUEUE = []


def build_fresh_wait_queue(today_date: date): # change to queue of all tech of the day()
    timeslots = []
    temp = list(timeSlots.objects.filter(date=today_date).values('tech', 'arrive_time'))
    for t in temp:
        if t['arrive_time'] != None:
            t['arrive_time'] = a = datetime.combine(date.min, t['arrive_time']) - datetime.min
            timeslots.append(t)
        
    lines = "_WAIT\n"
    sorted_list = sorted(timeslots, key=lambda x: x['arrive_time'])
    for sl in sorted_list:
        lines += f"{sl['tech']}:0\n"
    lines += "_WORK\n"
    f = open("helper/temp1", "w")
    f.write(lines)
    f.close()
    
    read_temp()
        
        
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
            if (z==1) and c != ":" :
                temp_num = c
    return ( ((''.join(temp_str)), int(temp_num)) )
# Function to sort the list of tuples by its second item
def Sort_Tuple(lst):
    global _WAIT_QUEUE
    _WAIT_QUEUE = (sorted(lst, key = lambda x: x[1]))

def read_temp():
    global _WAIT_QUEUE
    global _WORK_QUEUE
    f = open("helper/temp1", "r")
    lines = f.readlines()
    f.close()
    read_flag = 0
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

def get_WAIT_queue():
    read_temp()
    return _WAIT_QUEUE

def get_WORK_queue():
    read_temp()
    return _WORK_QUEUE

def main():
    build_fresh_wait_queue(date(2022,12,11))
    
    global _WAIT_QUEUE
    print(_WAIT_QUEUE)
    



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