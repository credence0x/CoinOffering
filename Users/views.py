from django.shortcuts import render,redirect
from Users.forms import CustomerForm,SignInForm
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from Users.models import Customer
from Coins.models import Coin


from django.contrib.auth.decorators import login_required



# Create your views here.

def SignUpController(request):
	if request.method == "POST":
		post_form = CustomerForm(request.POST)
		if post_form.is_valid():
			cd = post_form.cleaned_data
			user = User.objects.create_user(username=cd['username'],
			        						password=cd['password'],
			      				  			first_name = cd['first_name'],
			        						last_name=cd['last_name'],
			        						email=cd['email'])
			Customer.objects.create(user=user)
			login(request,user)
			request.session["new"] = True
			return HttpResponseRedirect(reverse('Users:home-page'))
		else:
			return render(request,'Users/sign_up.html',{'form':post_form})
	else:
		form = CustomerForm()
		return render(request,'Users/sign_up.html',
                          {'form':form})


def SignInController(request):
	if request.method == "POST":
		post_form = SignInForm(request.POST)
		if post_form.is_valid():
			cd = post_form.cleaned_data
			user = User.objects.get(email=cd['email'])
			checker = user.check_password(cd['password']) 
			if checker:
				login(request, user)
				return HttpResponseRedirect(reverse('Users:home-page'))
			else:
				post_form.add_error('email','Email and password did not match')
				return render(request,'Users/sign_in.html',
                        {'form':post_form})
		else:
			return render(request,'Users/sign_in.html',
                          {'form':post_form})
	else:
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('Users:home-page'))
		form = SignInForm()
		return render(request,'Users/sign_in.html',
                          {'form':form})
def LogOutController(request):
	logout(request)
	return HttpResponseRedirect(reverse('Users:sign-in'))
		
@login_required
def HomePageController(request):
	customer = request.user.customer
	coin=Coin.objects.get(name="MillionToken")
	try:
		bid = customer.bid
	except ObjectDoesNotExist:
		bid = False

	return render(request,'Users/home_page.html',
											{'coin':coin,
											'bid':bid})


def HomeRedirectController(request):
	return HttpResponseRedirect(reverse('Users:sign-in'))
