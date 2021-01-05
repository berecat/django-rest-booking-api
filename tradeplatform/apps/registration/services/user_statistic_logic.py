from django.utils import timezone

from apps.registration.models import UserProfile


def get_statistics_attribute(user_profile_id: int, to_date=None) -> dict:
    """Function return final dictionary, which contains correct field name"""

    if not to_date:
        to_date = timezone.now()

    response_data = {
        "quantity_trades": _count_all_trades(
            user_profile_id=user_profile_id, to_date=to_date
        ),
        "buy_money": _count_buy_money(user_profile_id=user_profile_id, to_date=to_date),
        "sell_money": _count_sell_money(
            user_profile_id=user_profile_id, to_date=to_date
        ),
    }

    return response_data


def _count_all_trades(user_profile_id: int, to_date):
    """Count all trades, which user has made"""

    user = UserProfile.objects.get(id=user_profile_id).user

    return (
        user.buyer_trade.all().filter(date__lte=to_date).count()
        + user.seller_trade.all().filter(date__lte=to_date).count()
    )


def _count_buy_money(user_profile_id: int, to_date):
    """The amount of money that the user spent to trades"""

    user = UserProfile.objects.get(id=user_profile_id).user

    quantity_money = 0
    for trade in user.buyer_trade.all().filter(date__lte=to_date):
        quantity_money += trade.unit_price * trade.quantity

    return quantity_money


def _count_sell_money(user_profile_id: int, to_date):
    """The amount of money that the user received from trades"""

    user = UserProfile.objects.get(id=user_profile_id).user

    quantity_money = 0
    for trade in user.seller_trade.all().filter(date__lte=to_date):
        quantity_money += trade.unit_price * trade.quantity

    return quantity_money
