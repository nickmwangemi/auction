import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from auctions.models import Auction, Listing


class Command(BaseCommand):
    help = "Seed the database with initial data for different auction statuses"

    def handle(self, *args, **kwargs):
        # Create or get users
        users = [
            User.objects.get_or_create(
                username="user1", defaults={"password": "password1"}
            )[0],
            User.objects.get_or_create(
                username="user2", defaults={"password": "password2"}
            )[0],
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

        # Function to create listings
        def create_listings(auction, status, start_offset, end_offset):
            for _ in range(20):  # Create 20 listings per auction
                car = random.choice(car_data)
                start_time = now + timedelta(days=start_offset)
                end_time = start_time + timedelta(days=7 + end_offset)
                Listing.objects.create(
                    auction=auction,
                    title=car["title"],
                    description=car["description"],
                    base_price=car["base_price"],
                    start_time=start_time,
                    end_time=end_time,
                )

        # Create upcoming auctions
        for i in range(4):  # Create 4 upcoming auctions
            start_time = now + timedelta(days=i + 1)
            auction, created = Auction.objects.get_or_create(
                auction_number=f"UPC00{i+1}",
                defaults={
                    "start_time": start_time,
                    "end_time": start_time + timedelta(days=7),
                    "status": "upcoming",
                },
            )
            create_listings(auction, "upcoming", i + 1, 0)

        # Create active auctions
        for i in range(4):  # Create 4 active auctions
            auction, created = Auction.objects.get_or_create(
                auction_number=f"ACT00{i+1}",
                defaults={
                    "start_time": now - timedelta(days=1),
                    "end_time": now + timedelta(days=5 + i),
                    "status": "active",
                },
            )
            create_listings(auction, "active", -1, i)

        # Create ended auctions
        for i in range(2):  # Create 2 ended auctions
            auction, created = Auction.objects.get_or_create(
                auction_number=f"END00{i+1}",
                defaults={
                    "start_time": now - timedelta(days=10 + i),
                    "end_time": now - timedelta(days=3 + i),
                    "status": "ended",
                },
            )
            create_listings(auction, "ended", -10 - i, 0)

        self.stdout.write(
            self.style.SUCCESS(
                """Successfully seeded the database with:
            - 4 upcoming auctions (UPC001-UPC004)
            - 4 active auctions (ACT001-ACT004)
            - 2 ended auctions (END001-END002)
            Each auction has 20 listings."""
            )
        )
