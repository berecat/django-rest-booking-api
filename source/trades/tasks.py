from celery import shared_task
from trades.services.trader_logic import create_trades_between_users


@shared_task()
def start_trade():
    """Start creating trades between users"""

    create_trades_between_users()
