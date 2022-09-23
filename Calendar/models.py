from django.db import models


# Create your models here.
class calendar (models.Model):
    date = models.DateField (blank=False)
    technicians = models.ManyToManyField ("Account.Technician",
                                          blank=True,

                                          )
