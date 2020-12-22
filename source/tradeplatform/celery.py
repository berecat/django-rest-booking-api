import os
from celery import Celery
from celery.schedules import crontab


app = Celery('tradeplatform')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'trader': {
        'task': 'trades.tasks.hello',
        'schedule': crontab(),
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))