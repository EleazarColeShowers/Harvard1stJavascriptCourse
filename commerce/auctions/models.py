from django.contrib.auth.models import AbstractUser
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class AuctionListing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey('User', on_delete=models.CASCADE)  # Use string 'User'
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    end_date = models.DateTimeField()
    image_url = models.URLField(blank=True)  
    active = models.BooleanField(default=True)  
    highest_bidder = models.ForeignKey('User', related_name='won_listings', on_delete=models.SET_NULL, null=True)  # Use string 'User'
    closed = models.BooleanField(default=False)
    watchlist = models.ManyToManyField('User', related_name='watchlisted_listings', blank=True)  # Use string 'User'
    
    def __str__(self):
        return self.title

class Bid(models.Model):
    bidder = models.ForeignKey('User', on_delete=models.CASCADE)  # Use string 'User'
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.bidder.username} - ${self.bid_amount}"

class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # Use string 'User'
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)  
    text = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class User(AbstractUser):
    watchlist = models.ManyToManyField(AuctionListing, related_name='watchlisted_users', blank=True)
