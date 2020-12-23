from celery import Celery
from celery.schedules import crontab


app = Celery('trader', include=['trades.tasks'])
app.autodiscover_tasks()
