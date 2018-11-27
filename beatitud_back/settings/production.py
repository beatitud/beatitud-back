from beatitud_back.settings.base import *

DEBUG = False

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 3600
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = False
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_DATABASE'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'beatitud.ctegnyot3xyq.eu-west-3.rds.amazonaws.com',
        'PORT': '5432',
        'TIMEZONE': 'UTC',
        'CONN_MAX_AGE': 500
    }
}
