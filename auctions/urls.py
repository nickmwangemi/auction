from django.urls import path
from .views import ListingListView, ListingDetailView, PlaceBidView, HomeView, SetAuctionView, CreateListingView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('listings/', ListingListView.as_view(), name='listing_list'),
    path('listing/<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
    path('listing/<int:listing_id>/bid/', PlaceBidView.as_view(), name='place_bid'),
    path('set-auction/', SetAuctionView.as_view(), name='set_auction'),
    path('create-listing/<int:auction_id>/', CreateListingView.as_view(), name='create_listing'),
]
