from django.db import models

# Create your models here.
class account_data(models.Model):
    username = models.CharField(max_length=30)
    key = models.CharField(max_length=30)
    value = models.CharField(max_length=30,null=True,blank=False)

    class Meta:
        unique_together = ("username", "key")