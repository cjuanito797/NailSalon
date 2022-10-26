from django.db import models
from Account.models import Technician, User
from django.urls import reverse


class Category (models.Model):
    name = models.CharField (max_length=200,
                             db_index=True)
    slug = models.SlugField (max_length=200,
                             unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse ('appointments:service_list_by_category',
                        args=[self.slug])


class subCategory (models.Model):
    categorty = models.ForeignKey ("Appointments.Category",
                                   on_delete=models.CASCADE,
                                   blank=False)
    name = models.CharField (max_length=200,
                             db_index=True)

    slug = models.SlugField (max_length=200, unique=True)


# Create your models here.
class Service (models.Model):
    category = models.ForeignKey (Category,
                                  on_delete=models.CASCADE,
                                  related_name='products',
                                  blank=True,
                                  default=None)
    name = models.CharField (max_length=30, db_index=True, blank=False)
    description = models.TextField (max_length=150, blank=False)
    slug = models.SlugField (max_length=30, db_index=True)
    price = models.DecimalField (max_digits=10, decimal_places=2)
    duration = models.DurationField (blank=False)
    image = models.ImageField (upload_to="services/%Y/%m/%d", blank=False)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        This will be utilized to link to a service description page, where we list more information
        :return:
        """

        return reverse ('appointments:service_detail',
                        args=[self.id, self.slug])


class Appointment (models.Model):
    services = models.ManyToManyField ("Appointments.Service",
                                       related_name='services',
                                       default=None,

                                       )
    customer = models.ForeignKey ("Account.User",
                                  on_delete=models.CASCADE,
                                  default=None,
                                  null=False)
    technician = models.ForeignKey ("Account.Technician",
                                    on_delete=models.CASCADE,
                                    default=None,
                                    null=True,
                                    blank=False)
    totalDuration = models.IntegerField ( )
    totalCharge = models.DecimalField (max_digits=10, decimal_places=2)
    start_time = models.TimeField ( )
    end_time = models.TimeField ( )
    date = models.DateField ( )
    details = models.TextField (blank=True, null=True)
    completed = models.BooleanField(default=False, null=True)

    def getTotalDuration(self):
        x = 0
        for service in services:
            x += service.duration
        self.totalDuration = x
        return self.totalDuration


class Sale (models.Model):
    service = models.ForeignKey (Service,
                                 on_delete=models.CASCADE,
                                 related_name='service')
    technician = models.ForeignKey (User,
                                    on_delete=models.CASCADE,
                                    related_name='technician')
    appointment = models.ForeignKey (Appointment,
                                     on_delete=models.CASCADE,
                                     related_name='appointment')
