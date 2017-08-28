import logging

from .base import *


WHITENOISE_MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware', ]
MIDDLEWARE = WHITENOISE_MIDDLEWARE + MIDDLEWARE

# Sentry
#INSTALLED_APPS += ['raven.contrib.django.raven_compact',]

# https://docs.sentry.io/clients/python/integrations/django/#message-references
#RAVEN_MIDDLEWARE = [
#    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware'
#]
#MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE

#SENTRY_DSN = env('DJANGO_SENTRY_DSN')
#SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT',
#                    default='raven.contrib.django.raven_compat.DjangoClient')
#SENTRY_CELERY_LOGLEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
#RAVEN_CONFIG = {
#    'CELERY_LOGLEVEL': env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO),
#    'DSN': SENTRY_DSN
#}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
