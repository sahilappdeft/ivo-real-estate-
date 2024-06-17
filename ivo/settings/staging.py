# Import base settings
from .base import *

# Override base settings for production
DEBUG = True
# ALLOWED_HOSTS = ['your_production_domain.com']

# Database settings for PostgreSQL

if os.getcwd() == "/home/ubuntu/IVO/ivo-real-estate/":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'ivodb',
            'USER': 'ivoportal',
            'PASSWORD': 'Psdnj@Eecezc3233r',
            'HOST': 'localhost',
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

EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=465
EMAIL_HOST_USER='a49722542@gmail.com'
EMAIL_HOST_PASSWORD='vmduiybtjqbirvcv'
EMAIL_USE_SSL=True