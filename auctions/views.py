from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, FormView, ListView

from .forms import AuctionForm, BidForm, ListingForm
from .models import Auction, Bid, Listing


class ListingListView(ListView):
    model = Listing
    template_name = "auctions/listing_list.html"
    context_object_name = "listings"


class ListingDetailView(DetailView):
    model = Listing
    template_name = "auctions/listing_detail.html"
    context_object_name = "listing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listing = self.get_object()
        bids = listing.bids.all()
        context["bids"] = bids
        context['current_best_offer'] = bids.order_by('-amount').first()
        context['winning_bid'] = listing.winning_bid()
        context['auction_status'] = listing.auction.update_status()
        return context


class PlaceBidView(LoginRequiredMixin, FormView):
    template_name = "auctions/place_bid.html"
    form_class = BidForm

    def form_valid(self, form):
        listing = get_object_or_404(Listing, id=self.kwargs["listing_id"])
        if timezone.now() < listing.start_time or timezone.now() > listing.end_time:
            messages.error(
                self.request, "Bidding is not allowed outside the trading window."
            )
            return self.form_invalid(form)

        bid = Bid.objects.create(
            listing=listing, user=self.request.user, amount=form.cleaned_data["amount"]
        )

        if bid.is_below_base_price:
            messages.warning(
                self.request,
                "Your bid is below the base price and may not be considered a winning bid.",
            )
        else:
            messages.success(self.request, "Your bid has been placed successfully.")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("listing_detail", kwargs={"pk": self.kwargs["listing_id"]})


class HomeView(ListView):
    model = Auction
    template_name = "auctions/home.html"
    context_object_name = "auctions"

    def get_queryset(self):
        queryset = Auction.objects.all()
        status = self.request.GET.get('status')
        if status and status != 'all':
            queryset = queryset.filter(status=status)
        return queryset


class SetAuctionView(LoginRequiredMixin, CreateView):
    model = Auction
    form_class = AuctionForm
    template_name = "auctions/set_auction.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Save the auction
        auction = form.save()
        # Redirect to create listings for this auction
        return redirect("create_listing", auction_id=auction.id)


class CreateListingView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = "auctions/create_listing.html"

    def get_initial(self):
        # Set the initial auction based on the URL parameter
        initial = super().get_initial()
        initial["auction"] = Auction.objects.get(id=self.kwargs["auction_id"])
        return initial

    def get_success_url(self):
        # Redirect back to the home page after creating a listing
        return reverse("home")
