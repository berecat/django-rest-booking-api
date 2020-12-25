from apps.trades.models import Offer
from apps.trades.services.db_interaction import (
    check_purchase_offer_user_balance, delete_offer_by_id,
    get_active_sell_offer_with_suitable_item, get_all_purchase_active_offers,
    get_available_quantity_stocks, get_item_id_related_to_offer,
    get_offer_by_id, get_user_by_id, get_user_id_related_to_offer)
from django.contrib.auth.models import User


def test_get_all_purchase_active_offers(offer_purchase_instance, offer_sell_instance):
    """Ensure that function correctly give us only offers with PURCHASE status"""

    offers = get_all_purchase_active_offers()

    assert len(offers) == 1
    assert offers[0] == offer_purchase_instance


def test_get_offer_by_id(offer_purchase_instance):
    """Ensure that function return right offer instance"""

    offer_id = offer_purchase_instance.id
    offer = get_offer_by_id(offer_id=offer_id)

    assert offer == Offer.objects.first()


def test_get_user_by_id(user_instance):
    """Ensure that function return right user instance"""

    user_id = user_instance.id
    user = get_user_by_id(user_id=user_id)

    assert user == User.objects.first()


def test_delete_offer_by_id(offer_purchase_instance):
    """Ensure that function correctly delete offer instance"""

    offer_id = offer_purchase_instance.id
    delete_offer_by_id(offer_id=offer_id)

    assert Offer.objects.first().is_active == False


def test_get_item_id_related_to_offer(offer_sell_instance):
    """Ensure that function returns correct id for item, which related to this offer"""

    offer_id = offer_sell_instance.id
    item_id = get_item_id_related_to_offer(offer_id=offer_id)

    assert item_id == Offer.objects.first().item.id


def test_get_user_id_related_to_offer(offer_sell_instance):
    """Ensure that function returns correct id for user, which related to this offer"""

    offer_id = offer_sell_instance.id
    user_id = get_user_id_related_to_offer(offer_id=offer_id)

    assert user_id == Offer.objects.first().user.id


def test_get_active_sell_offer_with_suitable_item(offer_instances):
    """Ensure that function return correct sell offers for purchase"""

    offers = get_active_sell_offer_with_suitable_item(
        offer_id=offer_instances[0].id, item_id=offer_instances[0].item.id
    )

    assert offers.count() == 2
    assert offers.first() == offer_instances[5]
    assert offers.last() == offer_instances[3]


def test_get_available_quantity_stocks(offer_purchase_instance):
    """
    Ensure that function return correct quantity of available stocks for now
    In purchase offer instance without current quantity
    """

    available_stocks = get_available_quantity_stocks(
        offer_id=offer_purchase_instance.id
    )

    assert available_stocks == 60


def test_get_available_quantity_stocks_with_current_quantity(offer_sell_instance):
    """
    Ensure that function return correct quantity of available stocks for now
    In sell offer instance with current quantity
    """

    available_stocks = get_available_quantity_stocks(offer_id=offer_sell_instance.id)

    assert available_stocks == 36


def test_check_purchase_offer_user_balance(offer_purchase_instance):
    """"""

    quantity = check_purchase_offer_user_balance(offer_id=offer_purchase_instance.id)

    assert quantity == 230
