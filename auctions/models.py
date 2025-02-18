from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Auction(models.Model):
    auction_number = models.CharField(max_length=50, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.auction_number

    def get_status(self):
        now = timezone.now()
        if now < self.start_time:
            return "Upcoming"
        elif self.start_time <= now <= self.end_time:
            return "Active"
        else:
            return "Ended"


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
