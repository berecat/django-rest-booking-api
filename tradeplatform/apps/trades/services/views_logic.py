from apps.trades.models import Offer


def get_average_offer_price():
    """Return average price from all offers"""

    all_price = 0
    for offer in Offer.objects.active():
        all_price += offer.price

    return all_price / Offer.objects.active().count()


def get_maximum_offer_price():
    """Return max price from all offers"""

    max_price = 0

    for offer in Offer.objects.active():
        max_price = offer.price

        if not Offer.objects.active().filter(price__gt=max_price).exists():
            break

    return max_price


def get_minimum_offer_price():
    """Return min price from all offers"""

    min_price = 0

    for offer in Offer.objects.active():
        min_price = offer.price

        if not Offer.objects.active().filter(price__lt=min_price).exists():
            break

    return min_price
