from django.db import models
from django.conf import settings


# Create your models here.


class Customer(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    related_name='customer',
                                    on_delete=models.CASCADE)
    # created customer models cus its extendable and also seperate from admin
    

