from django.db import models
from Account.models import Technician
from Appointments.models import Service, Appointment

class Sale(models.Model):
    service = models.ForeignKey(Service,
                                on_delete=models.CASCADE,
                                related_name='service')
    technician = models.ForeignKey(Technician,
                                on_delete=models.CASCADE,
                                related_name='technician')
    appointment = models.ForeignKey(Appointment,
                                on_delete=models.CASCADE,
                                related_name='appointment')
                                