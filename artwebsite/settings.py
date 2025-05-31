# artwebsite/settings.py

import os
from pathlib import Path
from urllib.parse import urlparse # For parsing GITPOD_WORKSPACE_URL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This should correctly point to 'ART-WEBSITE-DYNAMIC/' if settings.py is in 'ART-WEBSITE-DYNAMIC/artwebsite/'
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Core Django Settings ---

# SECRET_KEY is loaded from Gitpod Environment Variables
# Ensure DJANGO_SECRET_KEY is set in your Gitpod project settings.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    # In a real emergency where the env var isn't loading and you need to test,
    # you could temporarily hardcode it here, but immediately revert.
    # For now, raising an error is better to ensure it's set.
    raise ValueError("CRITICAL: No DJANGO_SECRET_KEY set in environment variables!")

# DEBUG status is loaded from Gitpod Environment Variables
# Set DJANGO_DEBUG to "True" (string) in Gitpod project settings for development.
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# ALLOWED_HOSTS configuration
ALLOWED_HOSTS = []

if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1']) # Standard local hosts
    
    gitpod_workspace_url_env = os.environ.get('GITPOD_WORKSPACE_URL')
    if gitpod_workspace_url_env:
        parsed_url = urlparse(gitpod_workspace_url_env)
        if parsed_url.hostname:
            ALLOWED_HOSTS.append(parsed_url.hostname.lower())
    
    # Add general Gitpod wildcard patterns as fallbacks or primary if GITPOD_WORKSPACE_URL isn't set
    ALLOWED_HOSTS.append('.gitpod.io')
    # If you know your specific Gitpod region consistently, e.g., 'ws-eu120':
    # ALLOWED_HOSTS.append('.ws-eu120.gitpod.io') 
    # You can add more regional patterns if you switch Gitpod regions:
    # ALLOWED_HOSTS.append('.ws-usXX.gitpod.io')

    # If you specifically set an ALLOWED_HOSTS_DEV environment variable in Gitpod,
    # its values will be added. This gives you an override.
    additional_dev_hosts_str = os.environ.get('ALLOWED_HOSTS_DEV')
    if additional_dev_hosts_str:
        ALLOWED_HOSTS.extend([host.strip().lower() for host in additional_dev_hosts_str.split(',')])

    ALLOWED_HOSTS = list(set(ALLOWED_HOSTS)) # Remove duplicates
else: 
    # Production settings for ALLOWED_HOSTS
    prod_hosts_str = os.environ.get('ALLOWED_HOSTS_PROD')
    if not prod_hosts_str:
        # It's critical to have this set in production.
        # You might want to raise an error or have a very restrictive default.
        print("WARNING: ALLOWED_HOSTS_PROD environment variable not set for production!")
        ALLOWED_HOSTS = [] # Or raise ImproperlyConfigured
    else:
        ALLOWED_HOSTS = [host.strip().lower() for host in prod_hosts_str.split(',')]


# --- Debugging Print Statements (Very useful for checking ALLOWED_HOSTS) ---
print(f"--- SETTINGS.PY (Loaded from artwebsite/settings.py) ---")
print(f"DJANGO_SECRET_KEY is: {'SET' if SECRET_KEY else 'NOT SET'}") # Don't print the key itself
print(f"DJANGO_DEBUG env var is: {os.environ.get('DJANGO_DEBUG')}")
print(f"DEBUG setting in Django is: {DEBUG}")
print(f"GITPOD_WORKSPACE_URL env var is: {os.environ.get('GITPOD_WORKSPACE_URL')}")
print(f"ALLOWED_HOSTS_DEV env var is: {os.environ.get('ALLOWED_HOSTS_DEV')}")
print(f"Computed ALLOWED_HOSTS in Django is: {ALLOWED_HOSTS}")
print(f"--- END SETTINGS.PY DEBUGGING ---")


# --- Application Definition ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Manages static files
    'taggit', 

    # Your apps
    'core.apps.CoreConfig', # Or simply 'core'

    # Third-party apps (uncomment and add to requirements.txt as you install them)
    # 'cloudinary',           # For Cloudinary integration (models, etc.)
    # 'cloudinary_storage',   # For Django storage backend with Cloudinary
    # 'taggit',               # For tagging functionality
    # 'ckeditor',             # For the rich text editor
    # 'ckeditor_uploader',    # For handling image uploads within CKEditor
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'artwebsite.urls' # This should be correct if your project config dir is 'artwebsite'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Optional project-level templates dir (e.g., for 404.html)
        'APP_DIRS': True, # Django will look for a 'templates' directory inside each app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Important for request object in templates
                'django.contrib.auth.context_processors.auth', # For user object
                'django.contrib.messages.context_processors.messages', # For displaying messages
                'core.context_processors.global_context', # Your custom context processor (e.g., for social links)
            ],
        },
    },
]

WSGI_APPLICATION = 'artwebsite.wsgi.application' # Correct if project config dir is 'artwebsite'


# --- Database ---
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Defaults to SQLite for simple Gitpod setup.
# For production, you'll use PostgreSQL via a DATABASE_URL environment variable.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', # Creates db.sqlite3 in your project root
    }
}
# Example for using DATABASE_URL (e.g., for PostgreSQL in production):
# import dj_database_url
# if 'DATABASE_URL' in os.environ and os.environ.get('DATABASE_URL'):
#     DATABASES['default'] = dj_database_url.config(
#         conn_max_age=600, # Optional: connection pooling
#         ssl_require=not DEBUG # Use SSL in production (common for cloud DBs)
#     )


# --- Password Validation ---
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Internationalization ---
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I1N = True # Corrected from USE_I18N in previous examples if that was a typo
USE_TZ = True


# --- Static files (CSS, JavaScript, Design Images) ---
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'
# Tells Django where to find static files within your apps (e.g., core/static/)
# For development, Django's runserver serves these automatically if APP_DIRS=True in TEMPLATES.
# STATICFILES_DIRS is for additional directories outside of apps, e.g., project-level static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static'), # Assuming your app is 'core' and has a 'static' subfolder
                                          # This will allow {% static 'core/css/main.css' %} if main.css is in core/static/core/css/
                                          # Or {% static 'css/main.css' %} if main.css is in core/static/css/
                                          # For clarity, usually core/static/core/css/main.css -> {% static 'core/css/main.css' %}
                                          # Or project_root/static/css/main.css -> {% static 'css/main.css' %} (if project_root/static is in STATICFILES_DIRS)
]
# For production, STATIC_ROOT is where 'collectstatic' will gather all static files.
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_production')


# --- Media files (User-uploaded content like images via Django Forms/Models if not directly to Cloudinary) ---
# https://docs.djangoproject.com/en/4.2/topics/files/
# If DEFAULT_FILE_STORAGE is Cloudinary, MEDIA_ROOT for local storage is mainly for temporary uploads or if some models don't use CloudinaryField.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# --- Default primary key field type ---
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Email Configuration (using SendGrid) ---
# Ensure EMAIL_HOST_PASSWORD (your SendGrid API Key) and
# DEFAULT_FROM_EMAIL_ADDRESS are set in your Gitpod Environment Variables.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # This is literally the string 'apikey' for SendGrid API key auth
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL_ADDRESS', 'Your Name <webmaster@localhost>') # Sensible fallback


# --- Cloudinary Configuration ---
# Ensure 'cloudinary' and 'cloudinary_storage' are in INSTALLED_APPS (after you pip install them).
# Ensure CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET are set in Gitpod Env Variables.
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    'SECURE': True, # Always use HTTPS for Cloudinary URLs
}
# This tells Django to use Cloudinary for all default file storage operations
# (e.g., for ImageField, FileField in your models, unless a specific CloudinaryField is used).
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage' # Add to INSTALLED_APPS: 'cloudinary_storage'


# --- CKEditor Configuration (Uncomment and configure after installing django-ckeditor and Pillow) ---
# Add 'ckeditor' and 'ckeditor_uploader' to INSTALLED_APPS.
# CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/" # This path is relative to MEDIA_ROOT if files are stored locally first.
                                          # With Cloudinary as DEFAULT_FILE_STORAGE, uploads should go there.
# CKEDITOR_IMAGE_BACKEND = 'pillow' # Pillow is needed for image processing during upload by CKEditor.
# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'full', # Or choose a more restricted toolbar configuration
#         'height': 300,
#         'width': 'auto', # Or specific width e.g. '100%'
#         # For image uploads with RichTextUploadingField, ensure your project's main urls.py includes:
#         # path('ckeditor/', include('ckeditor_uploader.urls')),
#     },
# }

# --- Messages framework (for displaying success/error messages in templates) ---
# Optional: If you use a CSS framework like Bootstrap and want to map Django message levels to its alert classes.
# from django.contrib.messages import constants as messages_constants
# MESSAGE_TAGS = {
#     messages_constants.DEBUG: 'alert-secondary',
#     messages_constants.INFO: 'alert-info',
#     messages_constants.SUCCESS: 'alert-success',
#     messages_constants.WARNING: 'alert-warning',
#     messages_constants.ERROR: 'alert-danger',
# }