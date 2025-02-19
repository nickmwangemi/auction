from rest_framework import serializers

from auctions.models import Bid, Listing, Auction


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'listing', 'user', 'amount', 'timestamp', 'is_below_base_price']
        read_only_fields = ['id', 'user', 'timestamp', 'is_below_base_price']

class ListingSerializer(serializers.ModelSerializer):
    bids = BidSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'auction', 'title', 'description', 'base_price', 'start_time', 'end_time', 'bids']
        read_only_fields = ['id', 'bids']

class AuctionSerializer(serializers.ModelSerializer):
    listings = ListingSerializer(many=True, read_only=True)

    class Meta:
        model = Auction
        fields = ['id', 'auction_number', 'start_time', 'end_time', 'status', 'listings']
        read_only_fields = ['id', 'listings']
