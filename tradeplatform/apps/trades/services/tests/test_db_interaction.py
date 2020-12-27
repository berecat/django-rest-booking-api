from apps.trades.models import Inventory, Offer, Trade
from apps.trades.services.db_interaction import (
    change_offer_current_quantity, change_user_balance_by_id,
    change_user_inventory, check_purchase_offer_user_balance, create_trade,
    delete_offer_by_id, get_active_sell_offer_with_suitable_item,
    get_all_purchase_active_offers, get_available_quantity_stocks,
    get_currency_by_id, get_full_price_of_trade, get_item_id_related_to_offer,
    get_offer_by_id, get_or_create_user_inventory, get_user_by_id,
    get_user_id_related_to_offer)


def test_get_all_purchase_active_offers(offer_purchase_instance, offer_sell_instance):
    """Ensure that function correctly give us only offers with PURCHASE status"""

    offers = get_all_purchase_active_offers()

    assert len(offers) == 1
    assert offers[0] == offer_purchase_instance


def test_get_offer_by_id(offer_purchase_instance):
    """Ensure that function return right offer instance"""

    offer_id = offer_purchase_instance.id
    offer = get_offer_by_id(offer_id=offer_id)

    assert offer == offer_purchase_instance


def test_get_user_by_id(user_instance):
    """Ensure that function return right user instance"""

    user_id = user_instance.id
    user = get_user_by_id(user_id=user_id)

    assert user == user_instance


def test_get_currency_by_id(default_currency_instance):
    """Ensure that function return right currency instance"""

    currency_id = default_currency_instance.id
    currency = get_currency_by_id(currency_id=currency_id)

    assert currency == default_currency_instance


def test_delete_offer_by_id(offer_purchase_instance):
    """Ensure that function correctly delete offer instance"""

    offer_id = offer_purchase_instance.id
    delete_offer_by_id(offer_id=offer_id)

    assert Offer.objects.first().is_active == False


def test_get_item_id_related_to_offer(offer_sell_instance):
    """Ensure that function returns correct id for item, which related to this offer"""

    offer_id = offer_sell_instance.id
    item_id = get_item_id_related_to_offer(offer_id=offer_id)

    assert item_id == offer_sell_instance.item.id


def test_get_user_id_related_to_offer(offer_sell_instance):
    """Ensure that function returns correct id for user, which related to this offer"""

    offer_id = offer_sell_instance.id
    user_id = get_user_id_related_to_offer(offer_id=offer_id)

    assert user_id == offer_sell_instance.user.id


def test_get_active_sell_offer_with_suitable_item(offer_instances):
    """Ensure that function return correct sell offers for purchase"""

    offers = get_active_sell_offer_with_suitable_item(offer_id=offer_instances[0].id)

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
    """Check quantity of money in offer's user"""

    quantity = check_purchase_offer_user_balance(offer_id=offer_purchase_instance.id)

    assert quantity == 230


def test_get_full_price_of_trade(offer_sell_instance):
    """Ensure that function return correct full price of trade"""

    full_price = get_full_price_of_trade(
        sell_offer_id=offer_sell_instance.id, quantity=80
    )

    assert full_price == 8000


def test_change_user_balance_by_id(user_instance):
    """Ensure that function change user's balance correctly"""

    change_user_balance_by_id(user_id=user_instance.id, money_quantity=80)
    user_balance = user_instance.balance.get()

    assert user_balance.quantity == 310


def test_get_or_create_user_inventory_with_not_exist_inventory(
    default_user_instance, item_instance
):
    """
    Ensure that function return correct inventory instance, which belong to request user
    With not existing inventory for received item
    """

    inventory = get_or_create_user_inventory(
        user_id=default_user_instance.id, item_id=item_instance.id
    )

    assert inventory == Inventory.objects.get(
        user_id=default_user_instance.id, item_id=item_instance.id
    )


def test_get_or_create_user_inventory_with_exist_inventory(
    default_user_instance, item_instance
):
    """
    Ensure that function return correct inventory instance, which belong to request user
    With existing inventory for received item
    """

    correct_inventory = Inventory.objects.create(
        user=default_user_instance, item=item_instance, quantity=100
    )
    inventory = get_or_create_user_inventory(
        user_id=default_user_instance.id, item_id=item_instance.id
    )

    assert inventory == correct_inventory


def test_change_user_inventory(default_user_instance, item_instance):
    """Ensure that function correctly change user's inventory"""

    change_quantity = 120
    change_user_inventory(
        user_id=default_user_instance.id,
        item_id=item_instance.id,
        quantity=change_quantity,
    )

    user_balance = default_user_instance.inventory.get()

    assert user_balance.quantity == change_quantity


def test_change_offer_current_quantity(offer_sell_instance):
    """Ensure that function correctly change offer's current quantity"""

    current_quantity = offer_sell_instance.quantity
    change_quantity = 76
    change_offer_current_quantity(
        offer_id=offer_sell_instance.id, quantity=change_quantity
    )

    assert Offer.objects.first().quantity == current_quantity + change_quantity


def test_create_trade_with_greatest_quantity_in_sell_offer(offer_instances):
    """
    Ensure that function correctly create Trade instance between users by the given offers
    The purchase offer instance has more quantity than sell offer
    """

    purchase_offer = offer_instances[0]
    sell_offer = offer_instances[5]

    create_trade(
        sell_offer_id=sell_offer.id,
        purchase_offer_id=purchase_offer.id,
        quantity=purchase_offer.quantity,
    )

    trade = Trade.objects.get()

    assert trade.item == sell_offer.item
    assert trade.seller == sell_offer.user
    assert trade.buyer == purchase_offer.user
    assert trade.quantity == purchase_offer.quantity
    assert trade.unit_price == sell_offer.price
    assert (
        trade.description
        == f"Trade between {sell_offer.user.username} and {purchase_offer.user.username}"
    )
    assert trade.seller_offer == sell_offer
    assert trade.buyer_offer == purchase_offer


def test_create_trade_with_greatest_quantity_in_purchase_offer(offer_instances):
    """
    Ensure that function correctly create Trade instance between users by the given offers
    The sell offer instance has more quantity than purchase offer
    """

    purchase_offer = offer_instances[0]
    sell_offer = offer_instances[4]

    create_trade(
        sell_offer_id=sell_offer.id,
        purchase_offer_id=purchase_offer.id,
        quantity=sell_offer.quantity,
    )

    trade = Trade.objects.get()

    assert trade.item == sell_offer.item
    assert trade.seller == sell_offer.user
    assert trade.buyer == purchase_offer.user
    assert trade.quantity == sell_offer.quantity
    assert trade.unit_price == sell_offer.price
    assert (
        trade.description
        == f"Trade between {sell_offer.user.username} and {purchase_offer.user.username}"
    )
    assert trade.seller_offer == sell_offer
    assert trade.buyer_offer == purchase_offer
