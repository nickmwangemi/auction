from django.core.management.base import BaseCommand
from auctions.models import Auction, Listing
from django.utils import timezone
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        # Create users
        user1 = User.objects.create_user(username='user1', password='password1')
        user2 = User.objects.create_user(username='user2', password='password2')

        # Create auctions
        auction1 = Auction.objects.create(
            auction_number='AUC001',
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=7)
        )

        auction2 = Auction.objects.create(
            auction_number='AUC002',
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=14)
        )

        # Create listings
        listing1 = Listing.objects.create(
            auction=auction1,
            title='2018 Honda Civic',
            description='A well-maintained 2018 Honda Civic.',
            base_price=15000.00,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=5)
        )

        listing2 = Listing.objects.create(
            auction=auction2,
            title='2020 Toyota Corolla',
            description='A brand new 2020 Toyota Corolla.',
            base_price=20000.00,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=10)
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
