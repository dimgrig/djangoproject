from django import forms
#from .models import *

class CheckoutContactForm(forms.Form):
    name= forms.CharField(required=True)
    phone=forms.CharField(required=True)
    email=forms.EmailField(required=True)

    #class Meta:
    #    model = Subscirber
    #    exclude = [""]