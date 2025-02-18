import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from auctions.models import Auction, Listing

class Command(BaseCommand):
    help = "Seed the database with initial data for different auction statuses"

    def handle(self, *args, **kwargs):
        # Create users
        users = [
            User.objects.create_user(username="user1", password="password1"),
            User.objects.create_user(username="user2", password="password2"),
        ]

        # List of car data
        car_data = [
            {
                "title": "2018 Honda Civic",
                "description": "A well-maintained 2018 Honda Civic.",
                "base_price": 15000.00,
            },
            {
                "title": "2020 Toyota Corolla",
                "description": "A brand new 2020 Toyota Corolla.",
                "base_price": 20000.00,
            },
            {
                "title": "2019 Ford Mustang",
                "description": "A sporty 2019 Ford Mustang.",
                "base_price": 25000.00,
            },
            {
                "title": "2017 BMW 3 Series",
                "description": "A luxurious 2017 BMW 3 Series.",
                "base_price": 30000.00,
            },
            {
                "title": "2021 Tesla Model 3",
                "description": "An electric 2021 Tesla Model 3.",
                "base_price": 40000.00,
            },
        ]

        now = timezone.now()

        # Create upcoming auctions
        for i in range(2):
            start_time = now + timedelta(days=i+1)
            auction = Auction.objects.create(
                auction_number=f"UPC00{i+1}",
                start_time=start_time,
                end_time=start_time + timedelta(days=7),
                status='upcoming'
            )

            Listing.objects.create(
                auction=auction,
                title=car_data[i]["title"],
                description=car_data[i]["description"],
                base_price=car_data[i]["base_price"],
                start_time=start_time,
                end_time=start_time + timedelta(days=7)
            )

        # Create active auctions
        for i in range(2):
            auction = Auction.objects.create(
                auction_number=f"ACT00{i+1}",
                start_time=now - timedelta(days=1),
                end_time=now + timedelta(days=5+i),
                status='active'
            )

            Listing.objects.create(
                auction=auction,
                title=car_data[i+2]["title"],
                description=car_data[i+2]["description"],
                base_price=car_data[i+2]["base_price"],
                start_time=now - timedelta(days=1),
                end_time=now + timedelta(days=5+i)
            )

        # Create ended auctions
        auction = Auction.objects.create(
            auction_number="END001",
            start_time=now - timedelta(days=10),
            end_time=now - timedelta(days=3),
            status='ended'
        )

        Listing.objects.create(
            auction=auction,
            title=car_data[4]["title"],
            description=car_data[4]["description"],
            base_price=car_data[4]["base_price"],
            start_time=now - timedelta(days=10),
            end_time=now - timedelta(days=3)
        )

        self.stdout.write(
            self.style.SUCCESS("""Successfully seeded the database with:
            - 2 upcoming auctions (UPC001, UPC002)
            - 2 active auctions (ACT001, ACT002)
            - 1 ended auction (END001)""")
        )