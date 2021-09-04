from django import forms
from django.contrib.auth.models import User



class BidForm(forms.Form):
    number_of_tokens = forms.CharField(widget=forms.NumberInput(
                                    attrs={'id':'number_of_tokens',
                                    'min':1}))
    price_per_token = forms.CharField(widget=forms.NumberInput(
                                    attrs={'id':'price_per_token',
                                    'min':1}))
   
