from apps.trades.models import Currency
from apps.trades.services.db_interaction import (change_user_inventory,
                                                 get_item_id_by_code,
                                                 get_or_create_user_balance,
                                                 get_or_create_user_inventory)


def setup_user_attributes(user_id: int, item_code: str) -> None:
    """Create Balance for user, if it doesn't exist now"""

    currency_id = _return_id_default_currency()
    item_id = get_item_id_by_code(item_code=item_code)

    get_or_create_user_balance(user_id=user_id, currency_id=currency_id)
    get_or_create_user_inventory(user_id=user_id, item_id=item_id)


def _return_id_default_currency() -> int:
    """Return id of default currency instance (USD)"""

    currency = Currency.objects.get_or_create(
        code="USD",
        defaults={"name": "American dollar"},
    )
    return currency[0].id
