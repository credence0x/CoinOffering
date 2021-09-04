from django.shortcuts import render
from Users.models import Customer
from Bid.models import Bid, SuccessfulBid, UnsuccessfulBid
from Coins.models import Coin


# Create your views here.
def run(coin_name="MillionToken"):
    # aDD STOP to bid model to know when to stop accepting
    global total_available_coins
    global skip

    coin = Coin.objects.get(name=coin_name)
    now = datetime.now()
    # if it isn't time
    if now < coin.end_bid_time:
        print("#####################  TEST NOT TIME YET   #####################")
        return
    total_available_coins = coin.number_available
    bids = Bid.objects.all().order_by('-price_per_token','timestamp')
    # doing database ordering cus it's faster
    initial_price = bids[0].price_per_token
    prices_dealt_with = [initial_price]
    same_price_allotment = {} # format is { bid : number_of_coins_allocated }. Default no allocated is 0
    #rename to allotment dictionary
    skip = False
    # whether_to_break_main_loop = False
    def address_group(group_dict):
        # all_globs = globals()
        global total_available_coins
        global skip
        print("............................NEW GROUP...........................")
        # if len(group_dict) == 1:
        #     bid = list(group_dict.keys())[0]
        #     if total_available_coins > bid.number_of_tokens :
        #         allotted = bid.number_of_tokens
        #         total_price_due = bid.price_per_token * allotted
        #         SuccessfulBid.objects.create(customer=bid.customer,
        #                                     bid = bid,
        #                                     number_of_tokens_allotted= allotted,
        #                                     total_price_due = total_price_due)
        # else:
        while True:
            done = False
            

            #list is used in line below to prevent RUNTIMEERROR DICT changed during iteration
            for each_bid,allotted in list(group_dict.items()):
                if total_available_coins > 0:
                    #if you get number of tokens request
                    if each_bid.number_of_tokens == allotted:
                        print(each_bid.customer.user.first_name,"  SUCCESSFUL  ", allotted, " / ", each_bid.number_of_tokens)
                        total_price_due = each_bid.price_per_token * allotted
                        SuccessfulBid.objects.create(customer=each_bid.customer,
                                                    bid = each_bid,
                                                    number_of_tokens_allotted= allotted,
                                                    total_due = total_price_due)

                        group_dict.pop(each_bid)
                        if len(group_dict)==0:
                            done = True
                    else:
                        group_dict[each_bid] +=1
                        total_available_coins-=1

                else:
                    # save all the ones that have been done
                    print("......................TOKEN EXHAUSTED.......................")
                    for each_bid,allotted in list(group_dict.items()):
                        
                        total_price_due = each_bid.price_per_token * allotted
                        if allotted >0:
                            print(each_bid.customer.user.first_name,"  SUCCESSFUL  ", allotted, " / ", each_bid.number_of_tokens)
                            SuccessfulBid.objects.create(customer=each_bid.customer,
                                                        bid = each_bid,
                                                        number_of_tokens_allotted= allotted,
                                                        total_due = total_price_due)
                        else:
                            # only callable from bool(same_price_allocation) below

                            UnsuccessfulBid.objects.create(customer=each_bid.customer)
                            print(each_bid.customer.user.first_name,"  FAILED  ", allotted, " / ", each_bid.number_of_tokens)

                    skip = True
            
                    return
                #update coins
                # print(total_available_coins)
                if done:
                    return
                


        group_dict = {}


    for bid in bids:
        print(bid.customer.user.first_name,bid.price_per_token,bid.timestamp)
    count = 0 
    len_bids = len(bids)

    for bid in bids:
        bid.processed=True
        bid.save()
        # intentionally put first to prevent conflict
        count+=1
        if not skip:
            address = False
            bid_price = bid.price_per_token
            if bid_price == prices_dealt_with[-1]:
                same_price_allotment[bid] = 0
                


            else:
                address_group(same_price_allotment)
                prices_dealt_with.append(bid_price)
                same_price_allotment = {}
                same_price_allotment[bid] = 0
                if count == len_bids:
                    # last one has been completed
                    # if this function isn't here, the last batch won't run
                    address_group(same_price_allotment)
                    # break

        else:
            if bool(same_price_allotment):
                address_group(same_price_allotment)
                same_price_allotment={}
            UnsuccessfulBid.objects.create(customer=bid.customer)
            print(bid.customer.user.first_name,"  FAILED  ", 0, " / ", bid.number_of_tokens)
    #save remaining coins
    print('.....ALL DONE......',total_available_coins," remaining")
