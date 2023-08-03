from __future__ import absolute_import, unicode_literals
import os
from statArchive.celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'statArchive.settings.dev')

app = Celery('statArchive')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() # Load task modules from all registered Django app configs.