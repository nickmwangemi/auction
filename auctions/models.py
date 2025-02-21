import logging

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class Auction(models.Model):
    AUCTION_STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("active", "Active"),
        ("ended", "Ended"),
    ]

    auction_number = models.CharField(max_length=50, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=10, choices=AUCTION_STATUS_CHOICES, default="upcoming"
    )
    # Flag to track if a notification has already been sent
    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.auction_number

    def clean(self):
        # Ensure that start_time is before end_time
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

    def get_status(self):
        now = timezone.now()
        if now < self.start_time:
            new_status = "upcoming"
        elif self.start_time <= now <= self.end_time:
            new_status = "active"
        else:
            new_status = "ended"

        # If status has changed, update and save.
        if new_status != self.status:
            self.status = new_status
            self.save()
        return self.status

    def notify_auction_end(self):
        # Only send notification if it hasn't been sent already.
        if self.notification_sent:
            return

        # Determine the winning bid and user
        winning_bid = None
        winning_user = None

        for listing in self.listings.prefetch_related('bids'):
            bid = listing.winning_bid()
            if bid and (
                winning_bid is None
                or bid.amount > winning_bid.amount
                or (
                    bid.amount == winning_bid.amount
                    and bid.timestamp < winning_bid.timestamp
                )
            ):
                winning_bid = bid
                winning_user = bid.user

        # Prepare the message data
        message_data = {
            "auction_number": self.auction_number,
            "title": f"Auction {self.auction_number} has ended.",
            "winning_bid": float(winning_bid.amount) if winning_bid else "No winning bid.",
            "winning_user": (
                winning_user.username if winning_user else "No winning user."
            ),
        }

        try:
            url = settings.WHATSAPP_SERVICE_URL
            response = requests.post(url, json=message_data, timeout=5)
            response.raise_for_status()
            # Mark the auction as notified if successful.
            self.notification_sent = True
            self.save(update_fields=["notification_sent"])
            logger.info(f"WhatsApp notification sent for auction {self.auction_number}")
        except Exception as e:
            logger.error("Error sending WhatsApp notification", exc_info=e)


class Listing(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="listings"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

    def clean(self):
        # Ensure listing dates fall within auction dates
        if self.start_time < self.auction.start_time:
            raise ValidationError(
                "Listing start time must be after the auction start time."
            )
        if self.end_time > self.auction.end_time:
            raise ValidationError(
                "Listing end time must be before the auction end time."
            )
        if self.start_time >= self.end_time:
            raise ValidationError(
                "Listing end time must be after the listing start time."
            )

    def winning_bid(self):
        # Get all bids for the listing, ordered by amount (descending) and timestamp (ascending)
        bids = self.bids.all().order_by("-amount", "timestamp")
        return bids.first() if bids else None

    def get_time_progress(self):
        if self.auction.status == "upcoming":
            return 0
        elif self.auction.status == "ended":
            return 100

        total_duration = (self.end_time - self.start_time).total_seconds()
        elapsed = (timezone.now() - self.start_time).total_seconds()
        progress = (elapsed / total_duration) * 100
        return min(max(progress, 0), 100)


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def is_below_base_price(self):
        return self.amount < self.listing.base_price

    def __str__(self):
        return f"Bid by {self.user.username} on {self.listing.title}"
