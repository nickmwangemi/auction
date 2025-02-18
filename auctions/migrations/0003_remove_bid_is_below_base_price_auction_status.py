# Generated by Django 5.1.6 on 2025-02-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_bid_is_below_base_price_alter_bid_listing_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bid",
            name="is_below_base_price",
        ),
        migrations.AddField(
            model_name="auction",
            name="status",
            field=models.CharField(
                choices=[
                    ("upcoming", "Upcoming"),
                    ("active", "Active"),
                    ("ended", "Ended"),
                ],
                default="upcoming",
                max_length=10,
            ),
        ),
    ]
