"""
WSGI config for beatitud_back project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# If DJANGO_SETTINGS_MODULE not given, then we take productions settings, be careful
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beatitud_back.settings.production')

application = get_wsgi_application()
