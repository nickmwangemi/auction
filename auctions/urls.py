from django.urls import path
from .views import ListingListView, ListingDetailView, PlaceBidView

urlpatterns = [
    path('', ListingListView.as_view(), name='listing_list'),
    path('listing/<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
    path('listing/<int:listing_id>/bid/', PlaceBidView.as_view(), name='place_bid'),
]
