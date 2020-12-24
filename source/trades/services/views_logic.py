from trades.models import Balance, Currency
from trades.services.db_interaction import get_currency_by_id, get_user_by_id


def setup_user_attributes(user_id: int) -> None:
    """Create Balance for user, if it doesn't exist now"""

    user = get_user_by_id(user_id=user_id)
    currency = get_currency_by_id(_return_id_default_currency())
    Balance.objects.get_or_create(user=user, currency=currency)


def _return_id_default_currency() -> int:

    currency = Currency.objects.get_or_create(
        code="USD",
        name="American dollar",
    )
    return currency[0].id
