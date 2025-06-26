import os
from datetime import timedelta
from celery import Celery

os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='config.settings')

app = Celery('config', broker=os.environ.get('CELERY_BROKER_URL'))
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "poll_machines": {
        "task": "analytics.tasks.poll_machines",
        "schedule": timedelta(seconds=15)
    },
    "check_metrics": {
        "task": "analytics.tasks.check_metrics",
        "schedule": timedelta(seconds=30)
    }
}

app.autodiscover_tasks()