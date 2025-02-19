import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Auction
from .utils import send_auction_completion_message


@receiver(post_save, sender=Auction)
def auction_completion_handler(sender, instance, **kwargs):
    if instance.status == "ended":
        phone_number = os.getenv("WHATSAPP_PHONE_NUMBER")
        auction_id = instance.auction_number
        item_description = (
            instance.listings.first().title
        )  # Assuming there's at least one listing
        winning_bid = instance.listings.first().bids.order_by("-amount").first()
        winning_user = winning_bid.user.username if winning_bid else "No bids"

        send_auction_completion_message(
            phone_number, auction_id, item_description, winning_bid, winning_user
        )
