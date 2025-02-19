import pywhatkit as kit
from django.utils import timezone


def send_auction_completion_message(
    phone_number, auction_id, item_description, winning_bid, winning_user
):
    # Current time
    now = timezone.now()
    hour = now.hour
    minute = (
        now.minute + 1
    )  # Adding one minute to ensure the message is sent in the next minute

    # Message content
    message = (
        "Auction Completed!\n"
        f"Auction ID: {auction_id}\n"
        f"Item: {item_description}\n"
        f"Winning Bid: {winning_bid}\n"
        f"Winning User: {winning_user}"
    )

    # Send the message
    kit.sendwhatmsg(phone_number, message, hour, minute)
