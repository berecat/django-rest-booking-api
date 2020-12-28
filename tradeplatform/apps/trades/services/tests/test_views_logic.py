from apps.trades.models import Balance, Currency, Inventory, Item
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


def test_setup_user_with_exist_attributes_with_default_currency_and_inventory(
    default_user_instance,
    default_currency_instance,
    item_instance,
):
    """
    Ensure that function correctly set user's attributes, which exists before testing
    But attribute Balance has not default currency.
    """

    inventory_quantity = 4536

    Balance.objects.create(
        user=default_user_instance,
        currency=default_currency_instance,
        quantity=1432,
    )
    Inventory.objects.create(
        user=default_user_instance, item=item_instance, quantity=inventory_quantity
    )
    setup_user_attributes(
        user_id=default_user_instance.id, item_code=item_instance.code
    )

    user_balance = default_user_instance.balance.get(currency__code="USD")
    user_inventory = default_user_instance.inventory.get(item__code=item_instance.code)

    assert user_balance.quantity == 1432
    assert user_balance.currency.code == default_currency_instance.code
    assert user_balance.currency.name == default_currency_instance.name
    assert user_inventory.quantity == inventory_quantity
    assert user_inventory.item.code == item_instance.code
    assert user_inventory.item.name == item_instance.name


def test_setup_user_with_exist_attributes_with_different_currency_and_inventory(
    default_user_instance, currency_instance, item_instance
):
    """
    Ensure that function correctly set user's attributes, which exists before testing
    But attribute Balance has default currency
    """

    item = Item.objects.create(code="AAPL", name="Apple")
    Balance.objects.create(
        user=default_user_instance,
        currency=currency_instance,
        quantity=1432,
    )
    Inventory.objects.create(
        user=default_user_instance,
        item=item,
        quantity=4535,
    )
    setup_user_attributes(
        user_id=default_user_instance.id, item_code=item_instance.code
    )

    user_balance = default_user_instance.balance.get(currency__code="USD")
    user_inventory = default_user_instance.inventory.get(item__code=item_instance.code)

    assert user_balance.quantity == 1000
    assert user_balance.currency.code == "USD"
    assert user_balance.currency.name == "American dollar"
    assert user_inventory.item.code == item_instance.code
    assert user_inventory.item.name == item_instance.name
    assert user_inventory.quantity == 1000


def test_setup_user_with_not_exist_attributes(default_user_instance, item_instance):
    """Ensure that function correctly set user's attributes which doesn't exist before testing"""

    setup_user_attributes(
        user_id=default_user_instance.id, item_code=item_instance.code
    )

    user_balance = default_user_instance.balance.get(currency__code="USD")
    user_inventory = default_user_instance.inventory.get(item__code=item_instance.code)

    assert user_balance.quantity == 1000
    assert user_balance.currency.code == "USD"
    assert user_balance.currency.name == "American dollar"
    assert user_inventory.quantity == 1000
    assert user_inventory.item.code == item_instance.code
    assert user_inventory.item.name == item_instance.name
