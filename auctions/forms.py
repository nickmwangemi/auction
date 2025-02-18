from django import forms
from django.utils import timezone

from .models import Auction, Listing


class BidForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["auction_number", "start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "base_price",
            "start_time",
            "end_time",
        ]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "auction": forms.Select(),  # Dropdown for auction selection
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
