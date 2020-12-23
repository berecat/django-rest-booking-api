from celery import Celery

app = Celery("trader", include=["trades.tasks"])
app.autodiscover_tasks()
