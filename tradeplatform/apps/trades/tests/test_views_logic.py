from apps.trades.services.views_logic import get_minimum_offer_price, get_maximum_offer_price, get_average_offer_price


def test_get_maximum_offer_price(offer_instances):
    """Ensure that function return maximum price from all offers"""

    average = get_maximum_offer_price()

    assert average == 50


def test_get_minimum_offer_price(offer_instances):
    """Ensure that function return minimum price from all offers"""

    average = get_minimum_offer_price()

    assert average == 5


def test_get_average_offer_price(offer_instances):
    """Ensure that function return average price from all offers"""

    average = get_average_offer_price()

    assert average == 14.125
