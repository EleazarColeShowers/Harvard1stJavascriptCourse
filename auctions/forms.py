# auctions/forms.py
from django import forms
from .models import AuctionListing, Category
from .models import Bid
from .models import Comment


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']

class ListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']