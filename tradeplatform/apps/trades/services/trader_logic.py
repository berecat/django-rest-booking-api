from apps.trades.services.db_interaction import (
    change_offer_current_quantity, change_user_balance_by_id,
    change_user_inventory, create_trade, delete_offer_by_id,
    get_active_sell_offer_with_suitable_item, get_all_purchase_active_offers,
    get_available_quantity_stocks, get_full_price,
    get_item_id_related_to_offer, get_offer_price_by_id,
    get_user_balance_quantity_by_offer_id, get_user_id_related_to_offer)


def create_trades_between_users() -> None:
    """Try to make trades with all purchase offers"""

    for purchase_offer in get_all_purchase_active_offers():
        _make_trades(offer_id=purchase_offer.id)


def _change_user_balance_by_offer_id(offer_id: int, money_quantity: int) -> None:
    """Change balance, which belong to the offer's user, by the specified amount"""

    user_id = get_user_id_related_to_offer(offer_id=offer_id)
    change_user_balance_by_id(user_id=user_id, money_quantity=money_quantity)


def _change_user_inventory_by_offer_id(offer_id: int, quantity: int) -> None:
    """Change inventory, which belong to the offer's user, by the specified amount"""

    user_id = get_user_id_related_to_offer(offer_id=offer_id)
    item_id = get_item_id_related_to_offer(offer_id=offer_id)
    change_user_inventory(user_id=user_id, item_id=item_id, quantity=quantity)


def _stocks_quantity_for_trade_by_given_offers(
    sell_offer_id: int, purchase_offer_id: int
) -> int:
    """Return final stocks quantity for trading"""

    sell_stocks = get_available_quantity_stocks(offer_id=sell_offer_id)
    purchase_stocks = get_available_quantity_stocks(offer_id=purchase_offer_id)

    if purchase_stocks <= sell_stocks:
        return purchase_stocks

    return sell_stocks


def _final_stocks_quantity_by_user_balance(
    sell_offer_id: int, purchase_offer_id: int
) -> int:
    """Return final quantity for trading in relation to user's balance"""

    quantity = _stocks_quantity_for_trade_by_given_offers(
        sell_offer_id=sell_offer_id, purchase_offer_id=purchase_offer_id
    )
    price = get_offer_price_by_id(offer_id=sell_offer_id)
    balance = get_user_balance_quantity_by_offer_id(offer_id=purchase_offer_id)

    ability_quantity = balance // price

    if ability_quantity <= quantity:
        return ability_quantity

    return quantity


def _prepare_for_trade(offer_id: int, money_quantity: int, quantity: int) -> None:
    """Change user's attributes and change current quantity for offer"""

    _change_user_balance_by_offer_id(offer_id=offer_id, money_quantity=money_quantity)
    _change_user_inventory_by_offer_id(offer_id=offer_id, quantity=quantity)
    change_offer_current_quantity(offer_id=offer_id, quantity=abs(quantity))


def _create_trade(sell_offer_id: int, purchase_offer_id: int) -> None:
    """Create trade for those offers"""

    final_quantity = _final_stocks_quantity_by_user_balance(
        sell_offer_id=sell_offer_id, purchase_offer_id=purchase_offer_id
    )
    full_price = get_full_price(
        sell_offer_id=sell_offer_id, quantity=final_quantity
    )

    _prepare_for_trade(
        offer_id=sell_offer_id, money_quantity=full_price, quantity=final_quantity
    )
    _prepare_for_trade(
        offer_id=purchase_offer_id, money_quantity=-full_price, quantity=-final_quantity
    )

    create_trade(
        sell_offer_id=sell_offer_id,
        purchase_offer_id=purchase_offer_id,
        quantity=final_quantity,
    )


def _check_offer_quantity(offer_id: int) -> bool:
    """
    Checking the offer for emptiness.
    If offer has no stocks function returns True.
    Otherwise returns False.
    """

    quantity = get_available_quantity_stocks(offer_id=offer_id)

    return not bool(quantity)


def _delete_empty_offer(offer_id: int) -> bool:
    """Delete empty offers. If offer has no stocks it will be deleted"""

    result = _check_offer_quantity(offer_id=offer_id)

    if result:
        delete_offer_by_id(offer_id=offer_id)

    return result


def _confirm_trade(sell_offer_id: int, purchase_offer_id: int) -> bool:
    """
    Validate information about trades
    Return true if user bought requested quantity of stocks
    """

    _create_trade(sell_offer_id=sell_offer_id, purchase_offer_id=purchase_offer_id)
    _delete_empty_offer(offer_id=sell_offer_id)

    return _delete_empty_offer(offer_id=purchase_offer_id)


def _make_trades(offer_id: int) -> None:
    """
    If user bought requested quantity of stocks function will be finished
    Otherwise continue to find suitable sell offers to make trades
    """

    suitable_sell_offers = get_active_sell_offer_with_suitable_item(offer_id=offer_id)

    for sell_offer in suitable_sell_offers:
        if _confirm_trade(purchase_offer_id=offer_id, sell_offer_id=sell_offer.id):
            break
