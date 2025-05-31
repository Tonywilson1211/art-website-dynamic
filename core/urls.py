# core/urls.py
from django.urls import path
from . import views # This imports views from the current directory (i.e., core/views.py)

app_name = 'core' # Optional: Define an app namespace for URL reversing if you have many apps

urlpatterns = [
    # This pattern routes the root path of this app (which will be the site's root
    # because of how we'll include it in the project's urls.py) to your home_view.
    path('', views.home_view, name='home'),
    path('gallery/', views.gallery_home_view, name='gallery_home'),
    path('artist/', views.about_view, name='about'), # Assuming 'artist.html' maps to your 'about' view
    path('blog/', views.blog_list_view, name='blog_list'),
    path('contact/', views.contact_view, name='contact'),

    # You will add other URL patterns for your 'core' app here later, for example:

    # path('blog/', views.blog_list_view, name='blog_list'),
    # path('blog/<slug:slug>/', views.blog_detail_view, name='blog_detail'),

    # path('gallery/category/<slug:category_slug>/', views.gallery_category_view, name='gallery_category_view'),
    # path('gallery/artwork/<slug:artwork_slug>/', views.artwork_detail_view, name='artwork_detail'),
    # path('gallery/api/all-artworks/', views.all_artworks_view, name='all_artworks_api'),
    # path('gallery/api/categories/', views.gallery_categories_api, name='gallery_categories_api'),
    # path('gallery/api/tags/', views.artwork_tags_api, name='artwork_tags_api'),
    # path('search/', views.search_artworks_view, name='search_artworks'),
    # path('subscribe-blog/', views.subscribe_to_blog_view, name='subscribe_to_blog'),
    # path('confirm-subscription/<uuid:token>/', views.confirm_subscription_view, name='confirm_subscription'),
    # path('unsubscribe/<uuid:token>/', views.unsubscribe_view, name='unsubscribe_blog'),
]