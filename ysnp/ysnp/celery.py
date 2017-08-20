import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ysnp.settings')

app = Celery('ysnp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
