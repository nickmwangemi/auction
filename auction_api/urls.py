from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuctionViewSet, BidViewSet, ListingViewSet

router = DefaultRouter()
router.register(r"auctions", AuctionViewSet)
router.register(r"listings", ListingViewSet)
router.register(r"bids", BidViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
