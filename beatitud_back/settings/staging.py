from beatitud_back.settings.base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_DATABASE'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'db',
        'PORT': '5432',
        'TIMEZONE': 'UTC'
    }
}