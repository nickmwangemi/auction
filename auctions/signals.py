from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Auction


@receiver(post_save, sender=Auction)
def auction_post_save(sender, instance, created, **kwargs):
    # Refresh the auction status (which updates status and sends notification if ended).
    current_status = instance.get_status()
    # If the status is ended and notification_sent is False, get_status() might not have
    # triggered notify_auction_end if the status hadn't changed.
    if current_status == "ended" and not instance.notification_sent:
        instance.notify_auction_end()
