# core/views.py
from django.shortcuts import render
from .models import HeroSlide, FeaturedHomepageArtwork # Import your new models

def home_view(request):
    active_hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')

    # Fetch up to 3 active featured artworks, ordered correctly
    featured_artworks_on_homepage = FeaturedHomepageArtwork.objects.filter(is_active=True).order_by('order')[:3]

    # We need the actual Artwork objects to get their images
    actual_featured_artworks = [fa.artwork for fa in featured_artworks_on_homepage if fa.artwork]

    context = {
        'hero_slides': active_hero_slides,
        'featured_artworks': actual_featured_artworks,
        # You can also fetch latest blog post here dynamically later
    }
    return render(request, 'core/home.html', context)