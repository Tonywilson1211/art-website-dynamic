# artwebsite/urls.py
from django.contrib import admin
from django.urls import path, include # Ensure 'include' is imported
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # This is the crucial line for your core app
    # path('ckeditor/', include('ckeditor_uploader.urls')), # You'll add this when setting up CKEditor
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Usually not needed for runserver with DEBUG=True