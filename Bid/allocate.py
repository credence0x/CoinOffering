from django.shortcuts import render
from Users.models import Customer
from Bid.models import Bid, SuccessfulBid, UnsuccessfulBid
from Coins.models import Coin
from datetime import datetime,timedelta
import pytz


# This is the code containing the main coin allocation logic
# In order to simplify the application, there is only one coin available and 
# its name is MillionToken
# run() is called by the scheduler in scheduler.categorise bids
# This process is scheduled because we need all data entries to produce accurate results

def _create_successful_bid(bid,allotted,total):
    SuccessfulBid.objects.create(customer=bid.customer,
                                bid = bid,
                                number_of_tokens_allotted= allotted,
                                total_due = total)
def _create_failed_bid(bid):
    UnsuccessfulBid.objects.create(customer=bid.customer)

def _print_successful_bid(bid,allotted):
    print(bid.customer.user.first_name,
            "  SUCCESSFUL  ", 
            allotted, "/",
             bid.number_of_tokens,
            bid.price_per_token,
             bid.timestamp)

def _print_failed_bid(bid,allotted):
    print(bid.customer.user.first_name,
            "  FAILED  ",
             allotted, 
             "/", 
             bid.number_of_tokens,
            bid.price_per_token,
             bid.timestamp)

def run(coin_name="MillionToken"):

    
    global total_available_coins
    global skip

    # This is here for the purpose of testing since we will have to recalculate
    # the allocation everytime a user makes a bid, 
    SuccessfulBid.objects.all().delete()
    UnsuccessfulBid.objects.all().delete()

    coin = Coin.objects.get(name=coin_name)
    now = datetime.now()
    when_we_can_calculate = coin.end_bid_time

    # If it is before the time to begin running, skip

    ############################# PREVIOUS SCHEDULE HANDLER #####################################
    # if now < when_we_can_calculate:

    #     print("#####################  ALMOST TIME TO CATEGORISE BIDS  #####################")
    #     return

    # # Immediately after a bid is made, the Coin's end_bid_time changes to 
    # # 10 seconds after the bid is made.  Given that the scheduler's refresh rate is 3 seconds,
    # # it must have tried at least 3 times(i.e 10//3 ) to reallocate
    # # and since we don't just want it to keep reallocating, the next condition
    # # makes it stop after reasonable time has been given to it to perform the function
    # if now > (when_we_can_calculate + timedelta(seconds=45)):
    # 	print("#####################  ALREADY DONE. SKIPPING  #####################")
    # 	return
    ################################################################################################


    total_available_coins = coin.number_available

    # doing database ordering because it's definitely faster
    # ordered my price_per_token first in descending order then
    #timestamp in ascending order (because we want earlier time first)
    bids = Bid.objects.all().order_by('-price_per_token','timestamp')


    # my solution to the problem is to arrange users in groups 
    # which are sorted according to the prices they are offering
    # this is done on the fly so we just need the initial price group first
    initial_price = bids[0].price_per_token
    price_group = [initial_price] # list of group prices. more values will be added on the fly
    allotment_dict = {} # format is { bid_object : number_of_coins_allocated }. Default n_o_c_a == 0
    skip = False
    # whether_to_break_main_loop = False
    def address_group(group_dict):
        global total_available_coins
        global skip
        print("########################  NEW BATCH  ########################")

        # This if statement just makes the code run efficiently.
        # It would still work with only the "else" block but by including the if statement,
        # the code doesn't have to loop before allocating coins to a single user
        bid = list(group_dict.keys())[0]
        if (len(group_dict) == 1) and total_available_coins and (total_available_coins > bid.number_of_tokens):
            # if its a single person group and coins are enough, just allot immediately
            allotted = bid.number_of_tokens
            total_price_due = bid.price_per_token * allotted
            _print_successful_bid(bid,allotted)
            _create_successful_bid(bid,allotted,total_price_due)
            total_available_coins-=allotted
        else:
            while True:
                done = False
                
                for each_bid,allotted in list(group_dict.items()):
                    if total_available_coins > 0:
                        #if you get number of tokens requested
                        if each_bid.number_of_tokens == allotted:
                            _print_successful_bid(each_bid,allotted)
                            total_price_due = each_bid.price_per_token * allotted
                            _create_successful_bid(each_bid,allotted,total_price_due)

                            

                            group_dict.pop(each_bid)

                            # if it has attended to all group members
                            if len(group_dict)==0:
                                done = True
                        else:
                            # give the user one token
                            group_dict[each_bid] +=1

                            total_available_coins-=1

                    else:
                        # tokens exhaused
                        # save the current progress
                        # print("######################## TOKENS HAVE BEEN EXHAUSTED ########################")
                        for each_bid,allotted in list(group_dict.items()):

                            total_price_due = each_bid.price_per_token * allotted
                         
                            if allotted >0:
                                _print_successful_bid(each_bid,allotted)
                                _create_successful_bid(each_bid,allotted,total_price_due)

                            else:
                                # only callable from bool(allotment_dict) below
                                _create_failed_bid(each_bid)
                                _print_failed_bid(each_bid,allotted)

                        skip = True
                        return
                    if done:
                        return
                    


            group_dict = {}
            # make sure to clear it after each batch


    # PRINT THE ORIGINAL DATA
    print("############################ DATA ORGANISED BY PRICE AND THEN TIMESTAMP ############################")
    print("First Name","Num Tokens","Price Per Token","TIMESTAMP",sep=" | ")
    for bid in bids:
        print(bid.customer.user.first_name,bid.number_of_tokens,bid.price_per_token,bid.timestamp,sep=" | ")
    print("###################################### END ORGANISED DATA #############################################" )

    





    ###############################
    ######## MAIN SYSTEM ##########
    ###############################

    
    count = 0 
    len_bids = len(bids)
    for bid in bids:
        bid.processed=True
        bid.save()
        count+=1
        # skip is True if all the tokens have been alloted 
        if not skip:
            bid_price = bid.price_per_token
            #  we are trying to get all members of a group here 
            # so if a bid qualifies, it is added 
            if bid_price == price_group[-1]:
                allotment_dict[bid] = 0 # { bid : 0 }

                

            # This means the person should be added to aa new group
            # before that howver, we address (allocate coins to) the last group 
            else:
                address_group(allotment_dict)
                price_group.append(bid_price)
                allotment_dict = {}
                allotment_dict[bid] = 0

                # if a person is in a last group, there is no next group to activate it
                # so that is addressed here
                if count == len_bids:
                    # if this function isn't here, the last batch won't run
                    address_group(allotment_dict)
                    # break

        else:
            if bool(allotment_dict):
                # this is here incase the next group isn't called because we ran out of coins 
                address_group(allotment_dict)
                allotment_dict={}
            # all are unsucessful as there are no coins
            _create_failed_bid(bid)
            _print_failed_bid(bid,0)
        
    
    # coin.number_available = 0
    # coin.save()
    # NOTE that i'm not saving the number of coins remaining for ease of testing 
    print("TOAL OF ",total_available_coins,"coins were not alloted")
    print('################   ALL DONE   ################')
