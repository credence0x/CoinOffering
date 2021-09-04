from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


# Create your models here.


class Coin(models.Model):
	# admin creator
    creator        = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    related_name='coins',
                                    on_delete=models.CASCADE)
    name = models.CharField(max_length=700)
    number_available = models.IntegerField(default=0)
    end_bid_time = models.DateTimeField()

