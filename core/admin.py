# core/admin.py
from django.contrib import admin
from .models import ( # Import all the models you will register from your core/models.py
    HeroSlide,
    FeaturedHomepageArtwork,
    GalleryCategory,
    Artwork,
    AdditionalArtworkImage, # If you have a separate admin class for this (though it's an inline for Artwork)
    InstagramImportedItem,
    BlogPost,
    Subscriber,
    SocialLink
    # Add any other models from core/models.py that you register here
)

# Now your @admin.register decorators and admin classes will work:

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'image_preview')
    list_editable = ('order', 'is_active')

    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(FeaturedHomepageArtwork)
class FeaturedHomepageArtworkAdmin(admin.ModelAdmin):
    list_display = ('artwork_title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    autocomplete_fields = ['artwork']

    def artwork_title(self, obj):
        return obj.artwork.title
    artwork_title.short_description = 'Artwork Title'

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug') # Assuming you added slug back or have it
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'representative_image')

class AdditionalArtworkImageInline(admin.TabularInline):
    model = AdditionalArtworkImage
    extra = 1
    max_num = 5
    fields = ('image', 'caption', 'order')

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_uploaded_display')
    list_filter = ('category', 'tags', 'date_uploaded')
    search_fields = ('title', 'description', 'tags__name', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AdditionalArtworkImageInline]
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'primary_image', 'description', 'category')}),
        ('Tags', {'fields': ('tags',)}),
    )
    def date_uploaded_display(self, obj): # Ensure this method is here if used in list_display
        return obj.date_uploaded.strftime("%Y-%m-%d %H:%M")
    date_uploaded_display.short_description = 'Date Uploaded'
    date_uploaded_display.admin_order_field = 'date_uploaded'


@admin.register(InstagramImportedItem)
class InstagramImportedItemAdmin(admin.ModelAdmin):
    list_display = ('instagram_post_id_link', 'image_preview', 'imported_at', 'status', 'linked_artwork_admin_link')
    list_filter = ('status', 'imported_at')
    readonly_fields = ('instagram_post_id', 'image_url_from_instagram', 'caption_from_instagram', 'imported_at', 'created_artwork', 'image_preview_readonly')
    actions = ['mark_as_pending_review', 'mark_as_ignored']
    # ... (rest of InstagramImportedItemAdmin methods as defined before) ...
    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image_url_from_instagram:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image_url_from_instagram)
        return "No Image URL"
    image_preview.short_description = 'Insta Preview'

    def image_preview_readonly(self, obj):
        return self.image_preview(obj)
    image_preview_readonly.short_description = 'Instagram Image Preview'

    def instagram_post_id_link(self, obj):
         return obj.instagram_post_id
    instagram_post_id_link.short_description = 'Instagram Post ID'

    def linked_artwork_admin_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        if obj.created_artwork:
            link = reverse(f"admin:{obj.created_artwork._meta.app_label}_{obj.created_artwork._meta.model_name}_change", args=[obj.created_artwork.pk])
            return format_html('<a href="{}">{}</a>', link, obj.created_artwork.title)
        return "-"
    linked_artwork_admin_link.short_description = 'Linked Website Artwork'

    def mark_as_pending_review(self, request, queryset):
        queryset.update(status='pending_review', created_artwork=None)
        self.message_user(request, f"{queryset.count()} item(s) marked as 'Pending Review'.")
    mark_as_pending_review.short_description = "Mark selected as 'Pending Review'"

    def mark_as_ignored(self, request, queryset):
        queryset.update(status='ignored', created_artwork=None)
        self.message_user(request, f"{queryset.count()} item(s) marked as 'Ignored'.")
    mark_as_ignored.short_description = "Mark selected as 'Ignored'"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'publish_date', 'was_published_recently')
    list_filter = ('publish_date', 'tags')
    search_fields = ('title', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    # ... (rest of BlogPostAdmin methods as defined before) ...
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username
    author_name.short_description = 'Author'

    def was_published_recently(self, obj):
        import datetime
        from django.utils import timezone
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= obj.publish_date <= now
    was_published_recently.admin_order_field = 'publish_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('confirmation_token', 'unsubscribe_token', 'subscribed_at')

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform_name', 'url', 'order', 'is_active')
    list_editable = ('url', 'order', 'is_active')

# Make sure any other models you are registering are also imported.