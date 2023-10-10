from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('listing/<int:listing_id>/', views.listing_details, name='listing_details'),
    path('auctions/<int:auction_id>/add_comment/', views.add_comment, name='add_comment'),
    path("watchlist/", views.watchlist, name="watchlist"),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_listings, name='category_listings'),
    path('', views.active_listings, name='active_listings'),
    path("", views.index, name="index"),  # Keep this last if needed
]

