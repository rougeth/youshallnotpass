"""
WSGI config for ysnp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ysnp.settings.local")

application = get_wsgi_application()

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'ysnp.settings.production':
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
    application = Sentry(application)
