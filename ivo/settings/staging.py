# Import base settings
from .base import *

# Override base settings for production
DEBUG = True
# ALLOWED_HOSTS = ['your_production_domain.com']

# Database settings for PostgreSQL

if os.getcwd() == "/home/ubuntu/IVO":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'ivodb',
            'USER': 'ivoportal',
            'PASSWORD': 'Psdnj@Eecezc3233r',
            'HOST': '13.202.134.230',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email settings
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = False

EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = '4aff3390a350e8'
EMAIL_HOST_PASSWORD = '8afd504e0e53c2'
EMAIL_PORT = '2525'