from apps.trades.models import Currency, Offer
from apps.trades.services.db_interaction import (get_available_quantity_stocks,
                                                 get_item_id_by_code,
                                                 get_or_create_user_balance,
                                                 get_or_create_user_inventory,
                                                 get_user_by_id)


def setup_user_attributes(user_id: int, item_code: str) -> None:
    """Create Balance for user, if it doesn't exist now"""

    currency_id = _return_id_default_currency()
    item_id = get_item_id_by_code(item_code=item_code)

    get_or_create_user_balance(user_id=user_id, currency_id=currency_id)
    get_or_create_user_inventory(user_id=user_id, item_id=item_id)


def check_user_quantity_stocks_for_given_item(
    user_id: int, item_code: str, quantity: str
) -> bool:
    """Check that user have enough quantity of stocks to sell"""

    user = get_user_by_id(user_id=user_id)

    inventory = user.inventory.get(item__code=item_code)
    item_id = get_item_id_by_code(item_code=item_code)

    if inventory:
        quantity_in_offers = _count_current_quantity_in_offers(
            user_id=user_id, item_id=item_id
        )

        if (inventory.quantity - quantity_in_offers) >= int(quantity):
            return True
        else:
            return False

    return quantity < 1000


def _count_current_quantity_in_offers(user_id: int, item_id: int) -> int:
    """Return number of quantity that user is selling right now"""

    quantity_in_offers = 0

    for offer in Offer.objects.sell_offers().filter(user_id=user_id, item_id=item_id):
        quantity = get_available_quantity_stocks(offer_id=offer.id)

        quantity_in_offers += quantity

    return quantity_in_offers


def _return_id_default_currency() -> int:
    """Return id of default currency instance (USD)"""

    currency = Currency.objects.get_or_create(
        code="USD",
        defaults={"name": "American dollar"},
    )
    return currency[0].id
