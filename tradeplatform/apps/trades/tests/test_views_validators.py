from apps.trades.services.db_interaction import (
    get_available_quantity_stocks,
    get_full_price,
)
from apps.trades.services.views_validators import (
    _count_current_money_quantity_in_offers,
    _count_current_quantity_in_offers,
    check_user_balance,
    check_user_quantity_stocks_for_given_item,
)


def test_count_current_quantity_in_offers(offer_instances):
    """Ensure that function return right quantity of stocks that are used in offers"""

    offer = offer_instances[2]

    quantity = _count_current_quantity_in_offers(
        user_id=offer.user.id, item_id=offer.item.id
    )

    assert quantity == 147


def test_check_user_quantity_stocks_for_given_item_with_greater_quantity(
    offer_sell_instance,
):
    """Ensure that function return correct boolean value if user hasn't enough quantity of stocks"""

    result = check_user_quantity_stocks_for_given_item(
        user_id=offer_sell_instance.user.id,
        item_id=offer_sell_instance.item.id,
        quantity="970",
    )

    assert result == False


def test_check_user_quantity_stocks_for_given_item_with_smaller_quantity(
    offer_sell_instance,
):
    """Ensure that function return correct boolean value if user has enough quantity of stocks"""

    result = check_user_quantity_stocks_for_given_item(
        user_id=offer_sell_instance.user.id,
        item_id=offer_sell_instance.item.id,
        quantity="900",
    )

    assert result == True


def test_count_current_money_quantity_in_offers(offer_instances):
    """Ensure that function return right quantity of stocks that are used in offers"""

    offer = offer_instances[0]

    quantity = _count_current_money_quantity_in_offers(
        user_id=offer.user.id,
    )

    assert quantity == get_full_price(
        sell_offer_id=offer.id,
        quantity=get_available_quantity_stocks(offer_id=offer.id),
    )


def test_count_current_money_quantity_in_offers_with_greater_quantity(offer_instances):
    """Ensure that function return correct boolean value if user hasn't enough quantity of stocks"""

    offer_purchase_instance = offer_instances[0]

    result = check_user_balance(
        user_id=offer_purchase_instance.user.id,
        quantity=get_available_quantity_stocks(offer_id=offer_purchase_instance.id),
        price=100000,
    )

    assert result == False


def test_count_current_money_quantity_in_offers_with_smaller_quantity(
    offer_purchase_instance,
):
    """Ensure that function return correct boolean value if user has enough quantity of stocks"""

    result = check_user_balance(
        user_id=offer_purchase_instance.user.id,
        quantity=get_available_quantity_stocks(offer_id=offer_purchase_instance.id),
        price=5,
    )

    assert result == True
