# core/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse
from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
import uuid # For tokens

# Define GalleryCategory first if Artwork uses it
class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Name of the art category.")
    slug = models.SlugField(unique=True, max_length=100, blank=True, help_text="Unique URL-friendly version of the name.")
    representative_image = CloudinaryField('gallery_category_representative_image', blank=True, null=True)
    # ... Meta, __str__, save, get_absolute_url methods ...
    class Meta:
        verbose_name_plural = "Gallery Categories"
        ordering = ['name']
    def __str__(self): return self.name
    def save(self, *args, **kwargs): # Basic slug generation
        from django.utils.text import slugify
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse('gallery_category_view', kwargs={'category_slug': self.slug})


# THEN define Artwork
class Artwork(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    primary_image = CloudinaryField('artwork_primary_image')
    description = models.TextField(blank=True)
    category = models.ForeignKey(GalleryCategory, on_delete=models.PROTECT, related_name='artworks')
    tags = TaggableManager(verbose_name="Artwork Tags", blank=True, related_name="artworks_tagged_directly") # Changed related_name
    date_uploaded = models.DateTimeField(auto_now_add=True, editable=False)
    # ... Meta, __str__, save, get_absolute_url methods ...
    class Meta:
        ordering = ['-date_uploaded']
    def __str__(self): return self.title
    def save(self, *args, **kwargs): # Basic slug generation
        from django.utils.text import slugify
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args, **kwargs) # Ensure unique slug logic if needed
    def get_absolute_url(self): return reverse('artwork_detail', kwargs={'artwork_slug': self.slug})


# THEN define AdditionalArtworkImage (if it depends on Artwork)
class AdditionalArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, related_name='additional_images', on_delete=models.CASCADE)
    image = CloudinaryField('artwork_additional_image')
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    # ... Meta, __str__ methods ...
    class Meta:
        ordering = ['order']
    def __str__(self): return f"Image for {self.artwork.title}"


# THEN HeroSlide (doesn't directly depend on Artwork for its definition)
class HeroSlide(models.Model):
    title = models.CharField(max_length=100, help_text="Title for the slide (shown on overlay).")
    image = CloudinaryField('hero_slide_image', help_text="Image for the hero slide.")
    link_url = models.URLField(max_length=255, blank=True, null=True, help_text="Optional URL this slide links to.")
    order = models.PositiveIntegerField(default=0, help_text="Order of display.")
    is_active = models.BooleanField(default=True, help_text="Display this slide?")
    # ... Meta, __str__ methods ...
    class Meta:
        ordering = ['order']
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"
    def __str__(self): return self.title


# THEN FeaturedHomepageArtwork (depends on Artwork)
class FeaturedHomepageArtwork(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, help_text="Select an artwork to feature on the homepage.")
    order = models.PositiveIntegerField(default=0, help_text="Order of display (1, 2, 3).")
    is_active = models.BooleanField(default=True, help_text="Display this featured artwork?")
    # ... Meta, __str__ methods ...
    class Meta:
        ordering = ['order']
        verbose_name = "Homepage Featured Artwork"
        verbose_name_plural = "Homepage Featured Artworks"
    def __str__(self): return f"{self.artwork.title} (Slot {self.order})"

class InstagramImportedItem(models.Model):
    instagram_post_id = models.CharField(max_length=255, unique=True, help_text="The unique ID of the Instagram post or media item.")
    image_url_from_instagram = models.URLField(max_length=1024, help_text="URL of the image directly from Instagram CDN.")
    caption_from_instagram = models.TextField(blank=True, help_text="The original caption from the Instagram post.")
    imported_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending_review', 'Pending Review'),
        ('processed', 'Processed into Artwork'),
        ('ignored', 'Ignored'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending_review')
    # Optional: Link to the Artwork created from this import
    created_artwork = models.OneToOneField(
        Artwork, # This links to your Artwork model defined above
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='source_instagram_item'
    )

    class Meta:
        ordering = ['-imported_at']
        verbose_name = "Instagram Imported Item"
        verbose_name_plural = "Instagram Imported Items"

    def __str__(self):
        return f"Instagram Import ({self.instagram_post_id}) - Status: {self.get_status_display()}"

# ... (SocialLink model definition as you have it) ...
# class SocialLink(models.Model):
# ...

class BlogPost(models.Model):
    title = models.CharField(max_length=200, help_text="The title of your blog post.")
    slug = models.SlugField(unique=True, max_length=255, blank=True, help_text="Unique URL-friendly version of the title (leave blank to auto-generate).")
    cover_image = CloudinaryField(
        'blog_cover_image', 
        blank=True,
        null=True,
        help_text="Optional: A cover image for the blog post."
    )
    content = RichTextUploadingField(
        help_text="Write your blog content here. You can format text and embed images."
    )
    summary = models.TextField(
        max_length=500,
        help_text="A short summary/excerpt for blog listing pages."
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Links to Django's User model
        on_delete=models.CASCADE,
        editable=False,
        help_text="The author of the post (automatically set)."
    )
    publish_date = models.DateTimeField(
        auto_now_add=True, # Automatically set when created
        editable=False,
        help_text="The date and time this post was published."
    )
    tags = TaggableManager(
        verbose_name="Blog Tags",
        help_text="Comma-separated list of tags. Artist can create new tags.",
        blank=True,
        # If Artwork model also has tags, you might need a unique 'through' model or different 'related_name'
        # For TaggableManager on BlogPost, if Artwork has a TaggableManager too,
        # ensure their related_names are different if you ever query from Tag to BlogPost/Artwork.
        # Example: related_name="blog_posts_tagged" (but often not needed if just using post.tags)
    )

    class Meta:
        ordering = ['-publish_date'] # Newest posts first
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        from django.utils.text import slugify # Import slugify here or at top of file
        if not self.slug: # If slug is not set
            self.slug = slugify(self.title)
            # Ensure uniqueness if multiple posts might have similar titles
            original_slug = self.slug
            counter = 1
            # Check if a post with this slug already exists (excluding self if updating)
            queryset = BlogPost.objects.filter(slug=self.slug)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            while queryset.exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
                queryset = BlogPost.objects.filter(slug=self.slug)
                if self.pk:
                    queryset = queryset.exclude(pk=self.pk)

        # Author setting is typically handled in the Admin's save_model method
        # if not self.pk and 'user' in kwargs: 
        #     self.author = kwargs.pop('user', None)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug}) # Assumes URL name 'blog_detail'

class Subscriber(models.Model):
    email = models.EmailField(unique=True, help_text="Email address of the subscriber.")
    is_active = models.BooleanField(default=False, help_text="True if the subscription is confirmed (double opt-in complete).")
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, help_text="Token for email confirmation.")
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, help_text="Token for unsubscribing.")
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Blog Subscriber"
        verbose_name_plural = "Blog Subscribers"

    def __str__(self):
        return f"{self.email} ({'Active' if self.is_active else 'Pending/Inactive'})"


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'), 
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter/X'), 
        ('pinterest', 'Pinterest'),
        ('linkedin', 'LinkedIn'), 
        ('other', 'Other')
    ]
    platform_name = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default='other')
    url = models.URLField(help_text="Full URL to your social media profile page")
    icon_svg_or_class = models.CharField(max_length=100, blank=True, help_text="Optional: SVG code for icon, or a CSS class name if using an icon font")
    is_active = models.BooleanField(default=True, help_text="Display this link on the site?")

    # THIS FIELD IS LIKELY MISSING OR MISNAMED IN YOUR FILE:
    order = models.PositiveIntegerField(default=0, help_text="Order of display (e.g., 0 first, 1 second)") 

    class Meta:
        ordering = ['order'] # This line needs the 'order' field defined above

    def __str__(self):
        return f"{self.get_platform_name_display()} Link"

# ... (other models like BlogPost, Subscriber, etc.) ...