from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManger

from Scheduling.models import TechnicianSchedule

# Create your models here.

class User (AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField (_ ('email'), unique=True)
    first_name = models.CharField (max_length=200)
    last_name = models.CharField (max_length=200)
    street_num = models.CharField (max_length=20)

    STATE_OPTIONS = (
        ('Alabama', 'Alabama'),
        ('Alaska', 'Alaska'),
        ('Arizona', 'Arizona'),
        ('Arkansas', 'Arkansas'),
        ('California', 'California'),
        ('Colorado', 'Colorado'),
        ('Conneticut', 'Conneticut'),
        ('Deleware', 'Deleware'),
        ('Florida', 'Florida'),
        ('Georgia', 'Georgia'),
        ('Hawaii', 'Hawaii'),
        ('Idaho', 'Idaho'),
        ('Illinois', 'Illinois'),
        ('Indiana', 'Indiana'),
        ('Iowa', 'Iowa'),
        ('Kansas', 'Kansas'),
        ('Kentucky', 'Kentucky'),
        ('Louisiana', 'Louisiana'),
        ('Maine', 'Maine'),
        ('Maryland', 'Maryland'),
        ('Massachusetts', 'Massachusetts'),
        ('Michigan', 'Michigan'),
        ('Minnesota', 'Minnesota'),
        ('Mississippi', 'Mississippi'),
        ('Missouri', 'Missouri'),
        ('Montana', 'Montana'),
        ('Nebraska', 'Nebraska'),
        ('Nevada', 'Nevada'),
        ('New Hampshire', 'New Hampshire'),
        ('New Jersey', 'New Jersey'),
        ('New Mexico', 'New Mexico'),
        ('New York', 'New York'),
        ('North Carolina', 'North Carolina'),
        ('North Dakota', 'North Dakota'),
        ('Ohio', 'Ohio'),
        ('Oklahoma', 'Oklahoma'),
        ('Oregon', 'Oregon'),
        ('Pennsylvania', 'Pennsylvania'),
        ('Rhode Island', 'Rhode Island'),
        ('South Carolina', 'South Carolina'),
        ('South Dakota', 'South Dakota'),
        ('Tennessee', 'Tennessee'),
        ('Texas', 'Texas'),
        ('Utah', 'Utah'),
        ('Vermont', 'Vermont'),
        ('Virginia', 'Virgina'),
        ('Washington', 'Washington'),
        ('West Virginia', 'West Virginia'),
        ('Wisconsin', 'Wisconsin'),
        ('Wyoming', 'Wyoming'),
    )

    state = models.CharField (max_length=15,
                              choices=STATE_OPTIONS,
                              blank=True,
                              default='Nebraska',
                              )
    zipcode = models.CharField (max_length=5, validators=[MinLengthValidator (5)])
    city = models.CharField (max_length=20)
    phoneNumber = models.CharField (max_length=10, validators=[MinLengthValidator (10)])
    isTechnician = models.BooleanField (default=False)
    is_staff = models.BooleanField (default=False)
    bio = models.TextField (blank=True)

    objects = CustomUserManger ( )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



class Technician (models.Model):
    user = models.OneToOneField ("Account.User",
                                 related_name='user',
                                 on_delete=models.CASCADE,
                                 default=None)
    bio = models.TextField (blank=True)


    schedule = models.OneToOneField("Scheduling.TechnicianSchedule",
                                   on_delete=models.CASCADE,
                                    default=True,
                                    blank=True)
    profilePicture = models.ImageField(upload_to='technicians/%Y/%m/%d',
                                       blank=True,
                                       default=None,
                                       null=True)

    def __str__(self):
        return self.user.email


class Customer (models.Model):
    user = models.OneToOneField ('Account.User',
                                 related_name='customer',
                                 on_delete=models.CASCADE,
                                 default=None)

    # add the appointment history here:

    bio = models.TextField (blank=True)


class Appointment (models.Model):
    phoneNumber = models.CharField (max_length=10, validators=[MinLengthValidator (10)])
