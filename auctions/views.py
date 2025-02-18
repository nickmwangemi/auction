from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Listing, Bid
from .forms import BidForm

class ListingListView(ListView):
    model = Listing
    template_name = 'auctions/listing_list.html'
    context_object_name = 'listings'

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'auctions/listing_detail.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listing = self.get_object()
        bids = Bid.objects.filter(listing=listing)
        current_best_offer = bids.order_by('-amount').first()
        context['bids'] = bids
        context['current_best_offer'] = current_best_offer
        return context

class PlaceBidView(LoginRequiredMixin, FormView):
    template_name = 'auctions/place_bid.html'
    form_class = BidForm

    def form_valid(self, form):
        listing = get_object_or_404(Listing, id=self.kwargs['listing_id'])
        Bid.objects.create(listing=listing, user=self.request.user, amount=form.cleaned_data['amount'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('listing_detail', kwargs={'pk': self.kwargs['listing_id']})
