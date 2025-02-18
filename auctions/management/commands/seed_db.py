from django.core.management.base import BaseCommand
from auctions.models import Auction, Listing
from django.utils import timezone
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        # Create users
        users = [
            User.objects.create_user(username='user1', password='password1'),
            User.objects.create_user(username='user2', password='password2')
        ]

        # List of car data
        car_data = [
            {'title': '2018 Honda Civic', 'description': 'A well-maintained 2018 Honda Civic.', 'base_price': 15000.00},
            {'title': '2020 Toyota Corolla', 'description': 'A brand new 2020 Toyota Corolla.', 'base_price': 20000.00},
            {'title': '2019 Ford Mustang', 'description': 'A sporty 2019 Ford Mustang.', 'base_price': 25000.00},
            {'title': '2017 BMW 3 Series', 'description': 'A luxurious 2017 BMW 3 Series.', 'base_price': 30000.00},
            {'title': '2021 Tesla Model 3', 'description': 'An electric 2021 Tesla Model 3.', 'base_price': 40000.00},
        ]

        # Create auctions dynamically
        for i, car in enumerate(car_data):
            auction = Auction.objects.create(
                auction_number=f'AUC00{i+1}',
                start_time=timezone.now(),
                end_time=timezone.now() + timezone.timedelta(days=7 + i*2)  # Stagger end times
            )

            Listing.objects.create(
                auction=auction,
                title=car['title'],
                description=car['description'],
                base_price=car['base_price'],
                start_time=timezone.now(),
                end_time=timezone.now() + timezone.timedelta(days=5 + i)  # Stagger end times
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with dynamic data'))
