# core/context_processors.py
from .models import SocialLink # Import your SocialLink model

def global_context(request):
    # This function makes its return dictionary available in all templates
    active_social_links = SocialLink.objects.filter(is_active=True).order_by('order')
    return {
        'social_links': active_social_links,
        # You can add other global context variables here later if needed
        # For example:
        # 'site_name': "Caroline J Hill Art",
    }