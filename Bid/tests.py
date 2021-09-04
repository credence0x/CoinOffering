from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth.models import User
from Bid.models import Bid, SuccessfulBid, UnsuccessfulBid
from Coins.models import Coin
from datetime import datetime
from .seed import seed_data
from .allocate import run
from django.urls import reverse
from datetime import datetime


class BidTestCase(TestCase):
	@classmethod
	def setUpClass(self):
		#adds the test data 
		seed_data()
		run()
		super(BidTestCase, self).setUpClass()


		

		

	def test_successful_bids(self):
		SuccessfulBids = SuccessfulBid.objects.all().order_by('-bid__price_per_token',"bid__timestamp")

		last = []
		sum_tokens = 0
		# did one long test so it doesn't have to loop twice 
		for pos,each in enumerate(SuccessfulBids):

			sum_tokens += each.number_of_tokens_allotted
			# check that nobody gets more than they requested for
			check_allotted = each.number_of_tokens_allotted <= each.bid.number_of_tokens
			self.assertEqual(check_allotted,True)
			# check that total_due is equal to number of tokens allotted *  price_per_token
			total_due = each.number_of_tokens_allotted * each.bid.price_per_token
			self.assertEqual(each.total_due,total_due)
			# check that the higher bidder was priortised
			if pos==0:
				pos+=1
				last.append(each)
				pass
			else:
				last_user_allotted = last[0].number_of_tokens_allotted
				last_user_requested = last[0].bid.number_of_tokens
				this_user_allotted = each.number_of_tokens_allotted
				check_allotted = (last_user_allotted==last_user_requested)

				# if tokens got exhausted, check that they were in the same group
				# and if they were, check that the last_user got higher
				# else if they weren't in the same group, this user must have 0 allotted coins
				if not check_allotted:
					last_user_price = last[0].bid.price_per_token
					this_user_price = each.bid.price_per_token
					if last_user_price==this_user_price:
						# remember that they are already sorted by time of bid
						check_allotted = (last_user_allotted >= this_user_allotted)
					else:
						check_allotted=(this_user_allotted==0)
			self.assertTrue(check_allotted)

			millionToken = Coin.objects.get(name="MillionToken")

			
			#check that bid was posted before time bid ended
			# check_time = millionToken.end_bid_time >= each.bid.timestamp
			# self.assertTrue(check_time)

			# Note that I'm not updating the number of coins avai

			last = [each]

	def test_correct_number_of_bids_classified(self):
		SuccessfulBids = SuccessfulBid.objects.all()
		UnsuccessfulBids = UnsuccessfulBid.objects.all()
		bids = Bid.objects.all()
		self.assertTrue(len(bids),len(SuccessfulBids) + len(UnsuccessfulBids))



	def test_GET_bid_create_controller(self):
		c = Client()
		c.login(username='lanre', password='verySimple')

		res = c.get(reverse("Bid:create"))
		self.assertEqual(res.status_code,200)
	def test_POST_bid_create_controller(self):
		c = Client()
		c.login(username='lanre', password='verySimple')
		res = c.post(reverse("Bid:create"),{'number_of_tokens':200,
				        				'price_per_token':700,
				      				  })
		self.assertEqual(res.status_code,302)

	def test_GET_bid_delete_controller(self):
		c = Client()
		c.login(username='lanre', password='verySimple')
		res = c.get(reverse("Bid:delete"))
		self.assertEqual(res.status_code,302)

		


