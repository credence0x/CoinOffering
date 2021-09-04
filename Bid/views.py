from django.shortcuts import render
from Users.models import Customer
from Bid.models import Bid, SuccessfulBid, UnsuccessfulBid
from Bid.forms import BidForm
from Coins.models import Coin
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,timedelta
from Bid import allocate



# Create your views here.
@login_required
def CreateController(request):
	user = request.user
	coin = Coin.objects.get(name="MillionToken")
	# load after one minute of bid
	coin.end_bid_time = datetime.now() + timedelta(seconds=30)
	coin.save()


	if request.method == "POST":
		post_form = BidForm(request.POST)
		if post_form.is_valid():
			cd = post_form.cleaned_data
			found = Bid.objects.filter(customer = user.customer).exists()
			if not found:
				bid = Bid.objects.create(number_of_tokens=cd['number_of_tokens'],
				        				price_per_token = cd['price_per_token'],
				      				  	timestamp = datetime.now(),
				      				  	customer=user.customer)


				# I used a scheduler previously but for ease of testing,i'll just call it immediately
				allocate.run()

			return HttpResponseRedirect(reverse('Users:home-page'))
		else:
			return render(request,'Bid/create.html',{'form':post_form,coin:coin})
	else:
		form = BidForm()
		return render(request,'Bid/create.html',
                          {'form':form,'coin':coin})
@login_required
def DeleteController(request):
	user = request.user
	try:
		bid = Bid.objects.get(customer = user.customer)

		# if not bid.processed:
		# 	bid.delete()
		# else:
		# 	request.session["message"] = "Could alter or delete bid because it has already been processed"
		
		try:
			UnsuccessfulBid.objects.get(customer=bid.customer).delete()
		except ObjectDoesNotExist:
			pass
		bid.delete() # successful bid gets deleted auto
	except ObjectDoesNotExist:
		pass
	return HttpResponseRedirect(reverse('Users:home-page'))
		