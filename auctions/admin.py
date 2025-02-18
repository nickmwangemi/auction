from django.contrib import admin
from .models import Auction, Listing, Bid

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('auction_number', 'start_time', 'end_time', 'listings_count')
    search_fields = ('auction_number',)
    ordering = ('start_time',)

    # Inline display of related listings
    def listings_count(self, obj):
        return obj.listings.count()
    listings_count.short_description = 'Listings Count'


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'auction', 'base_price', 'start_time', 'end_time', 'bids_count')
    search_fields = ('title', 'auction__auction_number')
    list_filter = ('auction',)
    ordering = ('start_time',)

    # Inline display of related bids
    def bids_count(self, obj):
        return obj.bids.count()
    bids_count.short_description = 'Bids Count'


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'amount', 'timestamp')
    search_fields = ('listing__title', 'user__username')
    list_filter = ('listing', 'user')
    ordering = ('-timestamp',)
