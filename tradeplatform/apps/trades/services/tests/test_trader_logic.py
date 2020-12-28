from apps.trades.models import Inventory, Offer, Trade
from apps.trades.services.db_interaction import (get_available_quantity_stocks,
                                                 get_offer_by_id)
from apps.trades.services.trader_logic import (
    _change_user_balance_by_offer_id, _change_user_inventory_by_offer_id,
    _check_offer_quantity, _confirm_trade, _create_trade, _delete_empty_offer,
    _final_stocks_quantity_by_user_balance, _make_trades, _prepare_for_trade,
    _stocks_quantity_for_trade_by_given_offers)


def test_change_user_balance_by_offer_id(offer_sell_instance):
    """Ensure that function correctly change user balance by the given offer's id and change quantity"""

    current_quantity = offer_sell_instance.user.balance.get().quantity
    change_quantity = 110

    offer_id = offer_sell_instance.id
    _change_user_balance_by_offer_id(offer_id=offer_id, money_quantity=change_quantity)

    user_balance = offer_sell_instance.user.balance.get()

    assert user_balance.quantity == current_quantity + change_quantity


def test_change_user_inventory_by_offer_id_with_not_exist_inventory(
    offer_purchase_instance,
):
    """
    Ensure that function correctly create and change user's inventory, related to offer's item
    With not exist inventory related to the given user and item
    """

    change_quantity = 100

    offer_id = offer_purchase_instance.id
    _change_user_inventory_by_offer_id(offer_id=offer_id, quantity=change_quantity)

    offer = get_offer_by_id(offer_id=offer_id)
    user_inventory = offer.user.inventory.get(item_id=offer.item.id)

    assert user_inventory.quantity == 1000 + change_quantity


def test_change_user_inventory_by_offer_id_with_exist_inventory(
    offer_purchase_instance,
):
    """
    Ensure that function correctly create and change user's inventory, related to offer's item
    With exist inventory related to the given user and item
    """

    current_quantity = 214
    change_quantity = 100

    offer_id = offer_purchase_instance.id
    Inventory.objects.create(
        user=offer_purchase_instance.user,
        item=offer_purchase_instance.item,
        quantity=current_quantity,
    )

    _change_user_inventory_by_offer_id(offer_id=offer_id, quantity=change_quantity)

    user_inventory = offer_purchase_instance.user.inventory.get(
        item_id=offer_purchase_instance.item.id
    )

    assert user_inventory.quantity == current_quantity + change_quantity


def test_stocks_quantity_for_trade_by_given_offers_with_greatest_purchase_quantity(
    offer_instances,
):
    """
    Ensure that function return correct stocks quantity for trade.
    Since purchase offer has more quantity of stocks than sell offer.
    Function has to return sell offer quantity of stocks.
    """

    purchase_offer = offer_instances[0]
    sell_offer = offer_instances[4]

    final_quantity = _stocks_quantity_for_trade_by_given_offers(
        sell_offer_id=sell_offer.id, purchase_offer_id=purchase_offer.id
    )

    assert final_quantity == get_available_quantity_stocks(offer_id=sell_offer.id)


def test_stocks_quantity_for_trade_by_given_offers_with_equal_quantity(offer_instances):
    """
    Ensure that function return correct stocks quantity for trade.
    Since purchase offer and sell offers have equal quantity of stocks,
    Function has to return sell offer and purchase offer quantity of stocks.
    """

    purchase_offer = offer_instances[0]
    sell_offer = offer_instances[6]

    final_quantity = _stocks_quantity_for_trade_by_given_offers(
        sell_offer_id=sell_offer.id, purchase_offer_id=purchase_offer.id
    )

    assert final_quantity == get_available_quantity_stocks(offer_id=sell_offer.id)
    assert final_quantity == get_available_quantity_stocks(offer_id=purchase_offer.id)


def test_stocks_quantity_for_trade_by_given_offers_with_greatest_sell_quantity(
    offer_instances,
):
    """
    Ensure that function return correct stocks quantity for trade.
    Since sell offer has more quantity of stocks than purchase offer.
    Function has to return purchase offer quantity of stocks.
    """

    purchase_offer_id = offer_instances[0].id
    sell_offer_id = offer_instances[5].id

    final_quantity = _stocks_quantity_for_trade_by_given_offers(
        sell_offer_id=sell_offer_id, purchase_offer_id=purchase_offer_id
    )

    assert final_quantity == get_available_quantity_stocks(offer_id=purchase_offer_id)


def test_final_stocks_quantity_by_user_balance_with_not_enough_money(offer_instances):
    """
    Ensure that function return correct quantity of stocks in the relation to user's balance
    Since user has not enough money, function has to return quantity of stocks that user can buy
    """

    purchase_offer = offer_instances[0]
    sell_offer = offer_instances[6]

    correct_quantity = purchase_offer.user.balance.get().quantity // sell_offer.price
    final_quantity = _final_stocks_quantity_by_user_balance(
        sell_offer_id=sell_offer.id, purchase_offer_id=purchase_offer.id
    )

    assert final_quantity == correct_quantity


def test_final_stocks_quantity_by_user_balance_with_enough_money_sell_offer_more_quantity(
    offer_instances,
):
    """
    Ensure that function return correct quantity of stocks in the relation to user's balance
    Since user has enough money and sell offer has more quantity of stocks than purchase offer,
    function has to return purchase offer's quantity of stocks
    """

    purchase_offer = offer_instances[7]
    sell_offer = offer_instances[5]

    final_quantity = _final_stocks_quantity_by_user_balance(
        sell_offer_id=sell_offer.id, purchase_offer_id=purchase_offer.id
    )

    assert final_quantity == get_available_quantity_stocks(offer_id=purchase_offer.id)


def test_final_stocks_quantity_by_user_balance_with_enough_money_purchase_offer_more_quantity(
    offer_instances,
):
    """
    Ensure that function return correct quantity of stocks in the relation to user's balance
    Since user has enough money and purchase offer has more quantity of stocks than sell offer,
    function has to return sell offer's quantity of stocks
    """

    purchase_offer = offer_instances[7]
    sell_offer = offer_instances[4]

    final_quantity = _final_stocks_quantity_by_user_balance(
        sell_offer_id=sell_offer.id, purchase_offer_id=purchase_offer.id
    )

    assert final_quantity == get_available_quantity_stocks(offer_id=sell_offer.id)


def test_prepare_for_trade(offer_purchase_instance):
    """Ensure that function correctly change user's and offer's attributes"""

    user = offer_purchase_instance.user
    current_money_quantity = user.balance.get().quantity
    current_offer_quantity = offer_purchase_instance.quantity
    money_quantity = 5443
    quantity = 3141

    offer_id = offer_purchase_instance.id

    _prepare_for_trade(
        offer_id=offer_id, money_quantity=money_quantity, quantity=quantity
    )

    user = offer_purchase_instance.user
    user_balance = user.balance.get()
    user_inventory = user.inventory.get(item_id=offer_purchase_instance.item)

    assert user_balance.quantity == current_money_quantity + money_quantity
    assert user_inventory.quantity == 1000 + quantity
    assert Offer.objects.get().quantity == current_offer_quantity + quantity


def test_check_offer_quantity_with_remaining_stocks(offer_sell_instance):
    """
    Ensure that function return right boolean response
    Since offer has the remaining stocks, function has to return False
    """

    result = _check_offer_quantity(offer_id=offer_sell_instance.id)

    assert result == False


def test_check_offer_quantity_without_remaining_stocks(offer_sell_instance):
    """
    Ensure that function return right boolean response
    Since offer hasn't the remaining stocks, function has to return True
    """

    offer_sell_instance.quantity = offer_sell_instance.entry_quantity
    offer_sell_instance.save()

    result = _check_offer_quantity(offer_id=offer_sell_instance.id)

    assert result == True


def test_delete_empty_offer_with_remaining_stocks(offer_purchase_instance):
    """
    Ensure that function return right boolean response and delete offer in right situations
    Since offer has the remaining stocks, function has to return False and hasn't to delete offer
    """

    result = _delete_empty_offer(offer_id=offer_purchase_instance.id)

    assert result == False
    assert Offer.objects.get().is_active == True


def test_delete_empty_offer_without_remaining_stocks(offer_purchase_instance):
    """
    Ensure that function return right boolean response and delete offer in right situations
    Since offer hasn't the remaining stocks, function has to return True and has to delete offer
    """

    offer_purchase_instance.quantity = offer_purchase_instance.entry_quantity
    offer_purchase_instance.save()

    result = _delete_empty_offer(offer_id=offer_purchase_instance.id)

    assert result == True
    assert Offer.objects.get().is_active == False


def test_create_trade_with_equal_quantity_stocks(offer_instances):
    """
    Ensure that function correctly crate Trade instance by the given offers
    """

    purchase_offer = offer_instances[0]
    sell_offer = offer_instances[6]

    buyer = purchase_offer.user
    seller = sell_offer.user

    original_buyer_balance = buyer.balance.get().quantity
    original_seller_balance = seller.balance.get().quantity

    correct_quantity = original_buyer_balance // sell_offer.price

    _create_trade(sell_offer_id=sell_offer.id, purchase_offer_id=purchase_offer.id)

    trade = Trade.objects.get()

    buyer_balance = buyer.balance.get().quantity
    buyer_inventory = buyer.inventory.get(item_id=purchase_offer.item).quantity

    seller_balance = seller.balance.get().quantity
    seller_inventory = seller.inventory.get(item_id=purchase_offer.item).quantity

    assert trade.item == purchase_offer.item
    assert trade.item == sell_offer.item
    assert trade.seller == sell_offer.user
    assert trade.buyer == purchase_offer.user
    assert trade.quantity == correct_quantity
    assert trade.unit_price == sell_offer.price
    assert (
        trade.description
        == f"Trade between {sell_offer.user.username} and {purchase_offer.user.username}"
    )
    assert trade.seller_offer == sell_offer
    assert trade.buyer_offer == purchase_offer
    assert buyer_balance == original_buyer_balance - (trade.unit_price * trade.quantity)
    assert seller_balance == original_seller_balance + (
        trade.unit_price * trade.quantity
    )
    assert buyer_inventory == 1000 - trade.quantity
    assert seller_inventory == 1000 + trade.quantity
