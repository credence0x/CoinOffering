from django.shortcuts import render
from django.contrib.auth.models import User
from Users.models import Customer
from Bid.models import Bid, SuccessfulBid, UnsuccessfulBid
from Coins.models import Coin
from datetime import datetime,timedelta


# Create your views here.
def run(*args):
    if 'delete' in args:
        test_users = User.objects.filter(username__icontains="test")
        for each in test_users:
            each.delete()
            print("deleted {} successfully".format(each))
        # Coin.objects.get(name="MillionToken").delete()
        # print("MillionToken deleted successfully")
            # Cascades make all other models deleted

    else:
        admin = User.objects.get(username="lanre")
        
        Coin.objects.create(creator=admin,
            name="MillionToken",
            number_available=22740,
            end_bid_time = datetime.now())
        
        

        print("MillionToken created successfully")
        

        customers = []
        ######## CREATE 20 USERS AND CUSTOMERS #######
        def new_user_data(num):
            # a number is added as suffix to make each field unique
            num = str(num)
            username = "test" + num
            password = "digiCentra123"
            first_name = username + "_first"
            last_name = username + "_last"
            email = username+"@digicentra.com"
            return username,password,first_name,last_name,email
        # Create 20 Users and Customer models
        print ("..........Creating 20 test Users...........")
        for num in range(20):
            username,password,first_name,last_name,email = new_user_data(num)
            new_user =  User.objects.create_user(username=username,
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)
            customer = Customer.objects.create(user=new_user)
            customers.append(customer)
            print("Successfully created user {}".format(num+1))

        ##########################################################

        # CREATE BIDS
       


        # I'm basically engineering the data so it covers scenerios 
        # in which the app will have to make sure that;  
        #       1. Unsucessful bids would be recorded 
        #       2. Successful bids will be recorded
        #       3. Price takes first priority
        #       4. Timestamps takes second priority
        #       5. Equal price bid are handled consequtively
        #       6. Ensure removal of bidder from queue and saving model once done
        count = 0
        no_tokens_for_less_than_4 = [2000,3000,1000,7000]
        price_for_less_than_4 = 20000
        old_timestamp = datetime.now() - timedelta(hours=2)
        for customer in customers:
            number_of_tokens = 700
            price_per_token = 18000
            timestamp = datetime.now()
            if count < 4:
                price_per_token = 20000
                number_of_tokens = no_tokens_for_less_than_4[count]
                if count == 3:
                    timestamp = old_timestamp
            elif count == 19:
                price_per_token = 15000     
            elif count == 18:
                price_per_token = 17000
                number_of_tokens = 2100
            elif count == 16:
                price_per_token = 17000
                number_of_tokens = 2100
            elif count == 15:
                price_per_token = 17000
                number_of_tokens = 2100
            elif count == 17:
                price_per_token = 14000


            
            
            Bid.objects.create(customer=customer,
                price_per_token=price_per_token,
                number_of_tokens=number_of_tokens,
                timestamp=timestamp)

            count+=1
