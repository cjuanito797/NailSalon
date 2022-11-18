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

#QUEUE CONTROL FUNCTIONS----------------------------------------------
# Build fresh queue in every day at open time salon open
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

# Clockin (backup) tech who arrive after fresh queue is created
def clock_tech_after_fresh_build(email):
    read_temp()
    low_priority = 0
    if len(_WAIT_QUEUE) > 0:
        low_priority = _WAIT_QUEUE[-1][1]
        
    if len(_WORK_QUEUE) > 0:
        if low_priority < _WORK_QUEUE[-1][1]:
            low_priority = _WORK_QUEUE[-1][1]
    _WAIT_QUEUE.append( (email, low_priority) )
    save_queue()

# Move chosen technician from Wait queue into Work queue
def wait_to_work(email):
    '''
    if len(_WAIT_QUEUE) >=1:
        a = _WAIT_QUEUE.pop(0)
        _WORK_QUEUE.append((a[0], a[1]+1))
        save_queue(_WAIT_QUEUE)
        return len(_WAIT_QUEUE)
    else:
        return 0
    '''
    read_temp()
    if len(_WAIT_QUEUE) >=1:
        for i in _WAIT_QUEUE:
            if i[0] == email:
                a = _WAIT_QUEUE.remove(i)
                _WORK_QUEUE.append( (i[0], i[1]+1) )
        save_queue()
        return len(_WAIT_QUEUE)
    else:
        return 0

# Move chosen technician from Work queue into Wait queue
def work_to_wait(email):
    read_temp()
    if len(_WORK_QUEUE) >=1:
        for i in _WORK_QUEUE:
            if i[0] == email:
                a = _WORK_QUEUE.remove(i)
                _WAIT_QUEUE.append(i)
        save_queue()
        return len(_WAIT_QUEUE)
    else:
        return 0



#BASIC FUNCTIONS-----------------------------------------------------------
# Retrieve technician waiting
def get_WAIT_queue():
    read_temp()
    return _WAIT_QUEUE

# Retrieve technician working
def get_WORK_queue():
    read_temp()
    return _WORK_QUEUE
     
# Sort data then write temp file
def save_queue():
    #Sort Tuple
    global _WAIT_QUEUE
    global _WORK_QUEUE
    _WAIT_QUEUE = (sorted(_WAIT_QUEUE, key = lambda x: x[1]))
    _WORK_QUEUE = (sorted(_WORK_QUEUE, key = lambda x: x[1]))
    #then write them in file
    write_temp()

# Read temp file
def read_temp():
    global _WAIT_QUEUE
    global _WORK_QUEUE
    f = open("helper/temp1", "r")
    lines = f.readlines()
    f.close()
    
    _WAIT_QUEUE = []
    _WORK_QUEUE = []
    
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

# Write temp file
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

# Split formatted string data into tuple  "email:priority" -> ("email", priority)
def to_tuple(line:str) -> tuple:
    temp_str = []
    temp_num =  []
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
def Sort_Tuple():
    global _WAIT_QUEUE
    global _WORK_QUEUE
    _WAIT_QUEUE = (sorted(_WAIT_QUEUE, key = lambda x: x[1]))
    _WORK_QUEUE = (sorted(_WORK_QUEUE, key = lambda x: x[1]))



def main():
    #build_fresh_wait_queue(date(2022,12,11))
    
    #global _WAIT_QUEUE
    #print(_WAIT_QUEUE)
    pass



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