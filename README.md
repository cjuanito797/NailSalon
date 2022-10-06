# NailSalon

This application serves as a scheduling system for a local nail salon.

A registered user may perform the following actions: 
  - log in to their account.
  - browse services that they may want to schedule an appointment for.
  - add services to their shopping list.
  - book an appointment selecting a technicinan -> time and date. 

In order to utilize this application, since it is not running on a webserver you would need to perform the following: 
  1. Clone a copy of the repository to a location on your desktop.
  2. Activate your virtual environment depending on your system. 
  3. Running the following commands (in order): 
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

