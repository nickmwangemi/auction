from django import forms
from django import forms
from .models import Auction, Listing

class BidForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['auction_number', 'start_time', 'end_time']

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['auction', 'title', 'description', 'base_price', 'start_time', 'end_time']
        widgets = {
            'auction': forms.HiddenInput(),  # Hide the auction field
        }
