# Generated by Django 4.1.7 on 2023-10-02 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_category_comment_bid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment_text',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='commenter',
            new_name='user',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='highest_bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_listings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlisted_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
