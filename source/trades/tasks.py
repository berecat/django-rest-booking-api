from celery import shared_task


@shared_task()
def create_trade():
    print("Hello world!")
