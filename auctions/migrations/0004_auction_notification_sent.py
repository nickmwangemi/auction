# Generated by Django 5.1.6 on 2025-02-20 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_remove_bid_is_below_base_price_auction_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="auction",
            name="notification_sent",
            field=models.BooleanField(default=False),
        ),
    ]
