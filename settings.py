# artwebsite/settings.py

import os
from pathlib import Path

# ... (BASE_DIR and other imports as before) ...

# --- Core Django Settings ---
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("No DJANGO_SECRET_KEY set in environment variables! Please set it in your Gitpod project settings.")

DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# ALLOWED_HOSTS configuration
if DEBUG:
    allowed_hosts_dev_str = os.environ.get('ALLOWED_HOSTS_DEV', 'localhost,127.0.0.1,.gitpod.io')
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_dev_str.split(',')]
else:
    prod_hosts = os.environ.get('ALLOWED_HOSTS_PROD')
    if not prod_hosts:
        print("WARNING: ALLOWED_HOSTS_PROD environment variable not set for production environment!")
        ALLOWED_HOSTS = []
    else:
        ALLOWED_HOSTS = [host.strip() for host in prod_hosts.split(',')]

# ADD THESE PRINT STATEMENTS FOR DEBUGGING:
print(f"--- SETTINGS.PY DEBUGGING ---")
print(f"DJANGO_DEBUG env var is: {os.environ.get('DJANGO_DEBUG')}")
print(f"DEBUG setting is: {DEBUG}")
print(f"ALLOWED_HOSTS_DEV env var is: {os.environ.get('ALLOWED_HOSTS_DEV')}")
print(f"Computed ALLOWED_HOSTS is: {ALLOWED_HOSTS}")
print(f"--- END SETTINGS.PY DEBUGGING ---")


# --- Application Definition ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'core.apps.CoreConfig', # Or simply 'core'

    # Third-party apps (uncomment and add as you install them via requirements.txt and pip)
    # 'cloudinary',
    # 'cloudinary_storage',
    # 'taggit',
    # 'ckeditor',
    # 'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Order matters, usually before auth
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'artwebsite.urls' # Replace 'artwebsite' if your project directory name is different

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Optional project-level templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.global_context', # For your social links, etc. (create this context processor in core app)
            ],
        },
    },
]

WSGI_APPLICATION = 'artwebsite.wsgi.application' # Replace 'artwebsite' if needed


# --- Database ---
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Default to SQLite for simple Gitpod setup.
# For production, you'll typically use PostgreSQL and configure it via a DATABASE_URL environment variable.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Example for using DATABASE_URL (e.g., for PostgreSQL in production):
# import dj_database_url
# if 'DATABASE_URL' in os.environ:
#     DATABASES['default'] = dj_database_url.config(
#         conn_max_age=600, # Optional: connection pooling
#         ssl_require=not DEBUG # Use SSL in production, not usually needed for local/dev DB
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
USE_I18N = True
USE_TZ = True # Timezone-aware datetimes are recommended


# --- Static files (CSS, JavaScript, Images for design) ---
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static'), # Make sure 'core' is your app name
]
# STATIC_ROOT is for production, used by 'python manage.py collectstatic'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_production')


# --- Media files (User-uploaded content if not all handled by Cloudinary directly) ---
# https://docs.djangoproject.com/en/4.2/topics/files/
# If DEFAULT_FILE_STORAGE is Cloudinary, MEDIA_ROOT for local storage might be less used.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # For any files that might be temporarily stored locally during uploads


# --- Default primary key field type ---
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Email Configuration (using SendGrid) ---
# Ensure you have set EMAIL_HOST_PASSWORD (your SendGrid API Key) and
# DEFAULT_FROM_EMAIL_ADDRESS in your Gitpod Environment Variables.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # This is literally the string 'apikey' for SendGrid API key auth
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL_ADDRESS', 'webmaster@localhost') # Fallback if not set


# --- Cloudinary Configuration ---
# Ensure 'cloudinary' and 'cloudinary_storage' are added to INSTALLED_APPS when you install them.
# Ensure CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET are set in Gitpod Env Variables.
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    'SECURE': True, # Use HTTPS for Cloudinary URLs
}
# This tells Django to use Cloudinary for all file uploads by default
# (e.g., for ImageField, FileField, and CloudinaryField in your models)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# --- CKEditor Configuration (Add these when you install and configure django-ckeditor) ---
# Ensure 'ckeditor' and 'ckeditor_uploader' are in INSTALLED_APPS.
# CKEDITOR_UPLOAD_PATH = "uploads/ckeditor_inline_images/" # This path is often relative to MEDIA_ROOT if files are stored locally first,
                                                        # OR will respect DEFAULT_FILE_STORAGE if configured correctly.
                                                        # With Cloudinary as DEFAULT_FILE_STORAGE, uploads should go there.
# CKEDITOR_IMAGE_BACKEND = 'pillow' # Pillow is needed for image processing
# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'full', # Or define a custom toolbar
#         'height': 300,
#         'width': '100%',
#         # You may need to configure filebrowserBrowseUrl and filebrowserUploadUrl
#         # if using specific CKEditor upload features or a custom storage for CKEditor uploads.
#         # Often, setting DEFAULT_FILE_STORAGE to Cloudinary is enough for RichTextUploadingField.
#     },
# }

# --- Messages framework (for displaying success/error messages in templates) ---
# Optional: Customize message tags for CSS frameworks like Bootstrap
# from django.contrib.messages import constants as messages_constants
# MESSAGE_TAGS = {
#     messages_constants.DEBUG: 'alert-secondary',
#     messages_constants.INFO: 'alert-info',
#     messages_constants.SUCCESS: 'alert-success',
#     messages_constants.WARNING: 'alert-warning',
#     messages_constants.ERROR: 'alert-danger',
# }