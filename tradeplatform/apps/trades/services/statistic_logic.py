from django.db.models import Avg, Max, Min

from apps.trades.models import Offer


def get_statistics_attribute():
    """Function return final dictionary. If dictionary contains None, it replaces to 0"""

    data = _get_statistic()

    if None in data.values():
        for key in data.keys():
            data[key] = 0

    return data


def _get_statistic():
    """Function return dictionary with Price average, max and min values"""

    return Offer.objects.active().aggregate(Avg("price"), Max("price"), Min("price"))
