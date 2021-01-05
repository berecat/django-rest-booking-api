from django.db.models import Avg, Max, Min
from django.utils import timezone

from apps.trades.models import Offer, Trade


def get_statistics_attribute(item_id: int, to_date=None) -> dict:
    """Function return final dictionary, which contains correct field name"""

    data = _convert_statistics_attribute(item_id=item_id, to_date=to_date)

    response_data = {
        "average_price": data["price__avg"],
        "max_price": data["price__max"],
        "min_price": data["price__min"],
        "sell_quantity_stocks": data["sell_quantity_stocks"],
    }

    return response_data


def _convert_statistics_attribute(item_id: int, to_date=None) -> dict:
    """Function convert dictionary. If dictionary contains None, it replaces to 0"""

    data = _get_statistic(item_id=item_id)

    if None in data.values():
        for key in data.keys():
            data[key] = 0

    data["sell_quantity_stocks"] = _get_stocks_data(item_id=item_id, to_date=to_date)

    return data


def _get_statistic(item_id: int) -> dict:
    """Function return dictionary with Price average, max and min values"""

    return (
        Offer.objects.active()
        .filter(item_id=item_id)
        .aggregate(Avg("price"), Max("price"), Min("price"))
    )


def _get_stocks_data(item_id: int, to_date=None) -> int:
    """Function return quantity of stocks sold by the given date"""

    quantity_stock = 0

    if not to_date:
        to_date = timezone.now()

    for trade in Trade.objects.all().filter(item_id=item_id, date__lte=to_date):
        quantity_stock += trade.quantity

    return quantity_stock
