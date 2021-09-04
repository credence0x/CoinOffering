from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth.models import User
from Bid.models import Bid, SuccessfulBid, UnsuccessfulBid
from Coins.models import Coin
from datetime import datetime
from Bid.seed import seed_data
from Bid.allocate import run
from django.urls import reverse
from datetime import datetime


class CoinTestCase(TestCase):
	# @classmethod
	# def setUpClass(self):
	# 	#adds the test data 
	# 	seed_data()
	# 	run()
	# 	super(CoinTestCase, self).setUpClass()


		

		

	def test_coin_count(self):
		SuccessfulBids = SuccessfulBid.objects.all().order_by('-bid__price_per_token',"bid__timestamp")
		sum_tokens = 0
		for each in SuccessfulBids:
			sum_tokens += each.number_of_tokens_allotted

		# check that we didn't allocate more than coins needed
		millionToken = Coin.objects.get(name="MillionToken")
		number_available = millionToken.number_available
		self.assertTrue(sum_tokens<=number_available)
			
		
		# Note that I'm not updating the number of coins available for ease of navigaing the code


	
		


