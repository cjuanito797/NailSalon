from django.db import models


# Create your models here.
class Service (models.Model):
    name = models.CharField (max_length=50, db_index=True, blank=False)
    description = models.TextField (max_length=150, blank=False)
    slug = models.SlugField (max_length=50, db_index=True)
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


class Appointment (models.Model):
    services = models.ManyToManyField ("Appointments.Service",
                                       related_name='services',
                                       default=None,
                                       )
    customer = models.ForeignKey ("Account.User",
                                  on_delete=models.CASCADE,
                                  default=None,
                                  null=False)
    totalDuration = models.IntegerField( )
    totalCharge = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()

    def getTotalDuration(self):
        x = 0
        for service in services:
            x += 1
        self.totalDuration = x
        return self.totalDuration
