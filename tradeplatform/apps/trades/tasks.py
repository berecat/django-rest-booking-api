from apps.trades.services.trader_logic import create_trades_between_users
from celery import shared_task


@shared_task()
def start_trade():
    """Start creating trades between users"""

    print("Hello world!")
