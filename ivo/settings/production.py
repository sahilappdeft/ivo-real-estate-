# Import base settings
from .base import *

# Override base settings for production
DEBUG = False
ALLOWED_HOSTS = ['your_production_domain.com']

# Database settings for PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Email settings for SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your_smtp_host'
EMAIL_PORT = 587  # Typically 587 for TLS or 465 for SSL
EMAIL_HOST_USER = 'your_smtp_username'
EMAIL_HOST_PASSWORD = 'your_smtp_password'
EMAIL_USE_TLS = True  # Set to True if your SMTP server requires TLS
EMAIL_USE_SSL = False  # Set to True if your SMTP server requires SSL
