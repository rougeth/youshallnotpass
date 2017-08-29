from .base import *


DEBUG = env.bool('DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# Query inspector
# https://github.com/dobarkod/django-queryinspect
MIDDLEWARE += (
    'qinspect.middleware.QueryInspectMiddleware',
)

QUERY_INSPECT_ENABLED = True

LOGGING = {
   'version': 1.0,
   'handlers': {
       'console': {
           'level': 'DEBUG',
           'class': 'logging.StreamHandler',
       },
   },
   'loggers': {
       'qinspect': {
           'handlers': ['console'],
           'level': 'DEBUG',
           'propagate': True,
       },
       'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
   },
}


# Celery
# All tasks will be executed locally by blocking until the task returns
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-always-eager
CELERY_ALWAYS_EAGER = True
