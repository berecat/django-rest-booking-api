from celery import Celery

app = Celery("trader", include=["apps.trades.tasks"])
app.autodiscover_tasks()
