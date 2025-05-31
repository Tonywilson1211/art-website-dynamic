import os
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # This is literally the string 'apikey' for SendGrid when using an API key as the password
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') # Or os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = '<caroline@cjhill-art.co.uk>' # See step below