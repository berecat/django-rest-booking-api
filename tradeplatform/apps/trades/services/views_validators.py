from apps.trades.models import Currency, Offer
from apps.trades.services.db_interaction import (get_available_quantity_stocks,
                                                 get_full_price,
                                                 get_or_create_user_balance,
                                                 get_or_create_user_inventory)


def setup_user_attributes(user_id: int) -> None:
    """Create Balance for user, if it doesn't exist now"""

    currency_id = _return_id_default_currency()
    get_or_create_user_balance(user_id=user_id, currency_id=currency_id)


def _return_id_default_currency() -> int:
    """Return id of default currency instance (USD)"""

    currency = Currency.objects.get_or_create(
        code="USD",
        defaults={"name": "American dollar"},
    )
    return currency[0].id


def check_user_quantity_stocks_for_given_item(
    user_id: int, item_id: int, quantity: str
) -> bool:
    """Check that user have enough quantity of stocks to sell"""

    inventory = get_or_create_user_inventory(user_id=user_id, item_id=item_id)

    quantity_in_offers = _count_current_quantity_in_offers(
        user_id=user_id, item_id=item_id
    )

    if (inventory.quantity - quantity_in_offers) >= int(quantity):
        return True

    return False


def check_user_balance(user_id: int, quantity: str, price: str) -> bool:
    """Check that user have enough money to buy certain quantity of stocks"""

    full_price = int(quantity) * int(price)

    default_currency_id = _return_id_default_currency()
    balance = get_or_create_user_balance(
        user_id=user_id, currency_id=default_currency_id
    )

    money_quantity = _count_current_money_quantity_in_offers(user_id=user_id)

    if (balance.quantity - money_quantity) < full_price:
        return False

    return True


def _count_current_money_quantity_in_offers(user_id: int) -> int:
    """Return quantity of money that user use in other offers"""

    money_in_offers = 0

    for offer in Offer.objects.purchase_offers().filter(user_id=user_id):
        quantity = get_full_price(
            sell_offer_id=offer.id,
            quantity=get_available_quantity_stocks(offer_id=offer.id),
        )

        money_in_offers += quantity

    return money_in_offers


def _count_current_quantity_in_offers(user_id: int, item_id: int) -> int:
    """Return number of quantity that user is selling right now"""

    quantity_in_offers = 0

    for offer in Offer.objects.sell_offers().filter(user_id=user_id, item_id=item_id):
        quantity = get_available_quantity_stocks(offer_id=offer.id)

        quantity_in_offers += quantity

    return quantity_in_offers
