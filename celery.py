import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'statArchive.settings')

# Create the Celery application
app = Celery('statArchive')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

