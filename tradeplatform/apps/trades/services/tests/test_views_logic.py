from apps.trades.models import Balance, Currency
from apps.trades.services.views_logic import (_return_id_default_currency,
                                              setup_user_attributes)


def test_return_id_default_with_exist_currency(default_currency_instance):
    """
    Ensure that _return_id_default_currency return correct id
    for the existing default currency
    """

    default_currency_id = _return_id_default_currency()

    assert default_currency_id == default_currency_instance.id


def test_return_id_default_with_not_exist_currency():
    """
    Ensure that _return_id_default_currency return correct id
    for the not existing default currency
    """

    default_currency_id = _return_id_default_currency()

    assert Currency.objects.count() == 1
    assert (
        default_currency_id
        == Currency.objects.get_or_create(
            code="USD", defaults={"name": "American dollar"}
        )[0].id
    )


def test_setup_user_with_exist_attributes_with_default_currency(
    default_user_instance, default_currency_instance
):
    """
    Ensure that function correctly set user's attributes, which exists before testing
    But attribute Balance has not default currency.
    """

    Balance.objects.create(
        user=default_user_instance,
        currency=default_currency_instance,
        quantity=1432,
    )
    setup_user_attributes(user_id=default_user_instance.id)

    user_balance = default_user_instance.balance.get(currency__code="USD")

    assert user_balance.quantity == 1432
    assert user_balance.currency.code == default_currency_instance.code
    assert user_balance.currency.name == default_currency_instance.name


def test_setup_user_with_exist_attributes_with_different_currency(
    default_user_instance, currency_instance
):
    """
    Ensure that function correctly set user's attributes, which exists before testing
    But attribute Balance has default currency
    """

    Balance.objects.create(
        user=default_user_instance,
        currency=currency_instance,
        quantity=1432,
    )
    setup_user_attributes(user_id=default_user_instance.id)

    user_balance = default_user_instance.balance.get(currency__code="USD")

    assert user_balance.quantity == 1000
    assert user_balance.currency.code == "USD"
    assert user_balance.currency.name == "American dollar"


def test_setup_user_with_not_exist_attributes(default_user_instance):
    """Ensure that function correctly set user's attributes which doesn't exist before testing"""

    setup_user_attributes(user_id=default_user_instance.id)

    user_balance = default_user_instance.balance.get(currency__code="USD")

    assert user_balance.quantity == 1000
    assert user_balance.currency.code == "USD"
    assert user_balance.currency.name == "American dollar"
