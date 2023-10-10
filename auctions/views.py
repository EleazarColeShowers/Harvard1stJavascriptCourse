from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import ListingForm, BidForm, CommentForm
from .models import AuctionListing, Bid, Comment, User
from django.contrib import messages  
from .models import Category




from .models import User


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect('index')  # Redirect to the homepage or wherever you want
    else:
        form = ListingForm()
        print("It worked")

    
    return render(request, 'auctions/create_listing.html', {'form': form})

def active_listings(request):
    active_listings = AuctionListing.objects.filter(active=True)
    return render(request, 'auctions/active_listings.html', {'active_listings': active_listings})

@login_required
def listing_details(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    bid_form = BidForm()
    comment_form = CommentForm()

    # Handle adding/removing from the watchlist
    if request.method == 'POST' and 'watchlist' in request.POST:
        if request.user in listing.watchlist.all():
            listing.watchlist.remove(request.user)
        else:
            listing.watchlist.add(request.user)

    # Handle bidding on the item
    if request.method == 'POST' and 'bid' in request.POST:
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid_amount = bid_form.cleaned_data['bid_amount']
            if bid_amount >= listing.starting_bid and (not listing.bids.exists() or bid_amount > listing.current_bid):
                bid = Bid(bidder=request.user, listing=listing, bid_amount=bid_amount)
                bid.save()
                listing.current_bid = bid_amount
                listing.save()
            else:
                # Handle bid error, e.g., display a message to the user
                pass

    # Handle closing the auction by the seller
    if request.method == 'POST' and 'close_auction' in request.POST:
        if request.user == listing.seller:
            listing.closed = True
            if listing.bids.exists():
                listing.highest_bidder = listing.bids.order_by('-bid_amount').first().bidder
            listing.active = False
            listing.save()

    # Handle adding a comment
    if request.method == 'POST' and 'add_comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data['comment_text']
            comment = Comment(commenter=request.user, listing=listing, comment_text=comment_text)
            comment.save()

    return render(request, 'auctions/listing_details.html', {
        'listing': listing,
        'bid_form': bid_form,
        'comment_form': comment_form
    })

def add_comment(request, listing_id):  # Change 'auction_id' to 'listing_id'
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.listing = listing  # Update to 'listing' instead of 'auction'
            comment.user = request.user
            comment.save()
            # Redirect to the listing detail page or wherever you want
            return redirect('listing_details', listing_id=listing_id)  # Update the redirect URL
    else:
        form = CommentForm()

    return render(request, 'auctions/add_comment.html', {'form': form})

@login_required
def watchlist(request):
    user = request.user
    print("It worked")
    watchlist_items = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"watchlist_items": watchlist_items})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'auctions/category_list.html', {'categories': categories})

def category_listings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    active_listings = AuctionListing.objects.filter(category=category, active=True)
    return render(request, 'auctions/category_listings.html', {'category': category, 'active_listings': active_listings})
