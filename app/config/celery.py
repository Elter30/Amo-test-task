import os
from datetime import timedelta
from celery.schedules import crontab
from celery import Celery

os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='config.settings')

app = Celery('config', broker=os.environ.get('CELERY_BROKER_URL'))
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "poll_machines": {
        "task": "analytics.tasks.poll_machines",
        "schedule": timedelta(minutes=15)
    }
}

app.autodiscover_tasks()