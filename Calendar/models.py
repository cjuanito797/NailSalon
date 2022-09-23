from django.db import models


# Create your models here.
class calendarEntry (models.Model):
    date = models.DateField (blank=False)
    technicians = models.ManyToManyField ("Account.Technician",
                                          blank=True, )
