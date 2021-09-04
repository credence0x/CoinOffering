from django.db import models

# Create your models here.
from Users.models import Customer
class Bid(models.Model):
    customer         			= models.OneToOneField(Customer,
                                     on_delete=models.CASCADE,
                                     related_name='bid',
                                    )
    number_of_tokens            = models.IntegerField(default=0)
    price_per_token 			= models.IntegerField(default=0)

    timestamp 					= models.DateTimeField()
    processed                     = models.BooleanField(default=False)
   # dont add any other field
    # def save():
    	# dont allow after time

    # total to be paid after successful


    # write logic to auto update bid in case it is changed 

class SuccessfulBid(models.Model):
    customer         			= models.OneToOneField(Customer,
                                     on_delete=models.CASCADE,
                                     related_name='successful_bid',
                                    )
    bid 						=  models.OneToOneField(Bid,
                                     on_delete=models.CASCADE,
                                     related_name='successful',
                                    )

    number_of_tokens_allotted   = models.IntegerField(default=0)
    total_due   				= models.IntegerField(default=0)


class UnsuccessfulBid(models.Model):
    customer         			= models.OneToOneField(Customer,
                                     on_delete=models.CASCADE,
                                     related_name='unsuccessful_bid',
                                    )
 
    
######As a final check, ensure that success and unsuccessful never have user present in both   
    


