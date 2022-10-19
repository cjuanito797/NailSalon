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

COMMAND = {'wait': ':WAIT\n', 'work': ':WORK\n'}
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
    


def main():
    f = open("helper/temp", "r")
    lines = f.readlines()
    z = 0
    for line in lines:
        line = line.replace('\n', '')
        if (line == "_WAIT"):
            pass
        else:
            if line != "_WORK" and z == 0:
                temp = line[1]
                _WAIT_QUEUE.append(temp)
            elif line == "_WORK":
                z = 1
            else:
                _WORK_QUEUE.append(line)
    
    a = _WAIT_QUEUE.pop(0)
    _WORK_QUEUE.append(a)
'''
# Function to sort the list of tuples by its second item
def Sort_Tuple(tup):
     
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):
         
        for j in range(0, lst-i-1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j]= tup[j + 1]
                tup[j + 1]= temp
    return tup
 
# Driver Code
tup =[('for', 24), ('is', 10), ('Geeks', 28),
      ('Geeksforgeeks', 5), ('portal', 20), ('a', 15)]
       
print(Sort_Tuple(tup))
'''
            
        
        

    print(_WAIT_QUEUE)
    print(_WORK_QUEUE)






    '''
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