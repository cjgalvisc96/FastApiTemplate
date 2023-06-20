from datetime import timedelta
from celery import Celery

# from celery.schedules import crontab

from backend.config import settings


beat_schedule = {
    'send_email': {
        'task': 'send_email',
        # 'schedule': crontab(minute=1),
        'schedule': timedelta(seconds=5),
    }
}

app_celery = Celery("backend")
app_celery.config_from_object(obj=settings.celery)
app_celery.conf.beat_schedule = beat_schedule
