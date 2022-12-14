# NailSalon

This application serves as a scheduling system for a local nail salon.

A registered user may perform the following actions: 
  - log in to their account.
  - browse services that they may want to schedule an appointment for.
  - add services to their shopping list.
  - book an appointment selecting a technicinan -> time and date. 

Requirements for running this application locally include: 
  - Having the latest version of python installed locally onto your machine.
  - Having a working IDE with a terminal window view, pycharm is a great choice.

In order to utilize this application, since it is not running on a webserver you would need to perform the following.  
  1. Clone a copy of the repository to a location on your desktop.


  2. Using your favorite IDE utilize the terminal window, or this may be done in the terminal window itself and make sure that you are in the correct path  for the project itself. 


  
  3. Activate your virtual environment depending on your system. Please see notes below on activating virtual environment. 


    You may need to install the virtual env itself to do this run the command: 
      pip install virtualenv
    
    Activate the virtual enviornment by running the following command: 
       venv\Scripts\Activate
       
    Install the requirements.txt 
      pip install -r requirements.txt
    
    
  4. Running the following commands (in order): 
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    
    
Release Notes
- The current state of our appliication sees there being a  complete hybrid implementatiion. Currently these are the features that are working. 

Customer End
- Can schedule an appointment with a technician at a given date and time. 
- Can re-schedule their appointment
- Can cancel an appointment
- Can view details of an upcoming appointment
- Can schedule an appointment with a technician that will be assigned to them upon arrival. 
- Can perform CRUD operations on their application such as: changing their e-mail, password, etc. 

Technician End
- Can manage their upcoming appointments. 

Management End
- Can manage customers as they walk in.
- Can create new technicians through a hiring portal
- Can create an appointment for a registered user or a walk-in client.

