from typing import Optional

from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from apps.trades.models import Balance, Currency, Inventory, Item, Offer, Trade


def get_all_purchase_active_offers() -> QuerySet:
    """Return all active offer instances with PURCHASE status"""

    return Offer.objects.purchase_offers()


def get_offer_by_id(offer_id: int) -> Optional[Offer]:
    """Return offer by it's id"""

    return Offer.objects.get(id=offer_id)


def get_user_by_id(user_id: int) -> Optional[User]:
    """Return user by id"""

    return User.objects.get(id=user_id)


def get_currency_by_id(currency_id: int) -> Optional[Currency]:
    """Return currency by id"""

    return Currency.objects.get(id=currency_id)


def get_offer_price_by_id(offer_id: int) -> int:
    """Return offer's price by the given offer's id"""

    offer = get_offer_by_id(offer_id=offer_id)

    return offer.price


def get_user_balance_quantity_by_offer_id(offer_id: int) -> int:
    """Return user's quantity of money in his balance"""

    offer = get_offer_by_id(offer_id=offer_id)
    user_balance = offer.user.balance.get(currency__code="USD")

    return user_balance.quantity


def delete_offer_by_id(offer_id: int) -> None:
    """Delete a offer by it's id"""

    offer = get_offer_by_id(offer_id=offer_id)
    offer.is_active = False
    offer.save()


def get_item_id_related_to_offer(offer_id: int) -> int:
    """Return id of item related to the current offer"""

    offer = get_offer_by_id(offer_id=offer_id)
    return offer.item.id


def get_user_id_related_to_offer(offer_id: int) -> int:
    """Return user instance related to the current offer"""

    offer = get_offer_by_id(offer_id=offer_id)
    return offer.user.id


def get_active_sell_offer_with_suitable_item(offer_id: int) -> QuerySet:
    """
    Return all active offer with SELL status and current item,
    ordering by price in ascending order. The best offers come first in QuerySet
    """

    offer = get_offer_by_id(offer_id=offer_id)
    sell_offers = (
        Offer.objects.sell_offers()
        .filter(item__id=offer.item.id, price__lte=offer.price)
        .order_by("price")
        .exclude(user__id=offer.user.id)
    )

    return sell_offers


def get_available_quantity_stocks(offer_id: int) -> int:
    """Return the quantity of stocks in offer that are available for trading now"""

    offer = get_offer_by_id(offer_id=offer_id)
    return offer.entry_quantity - offer.quantity


def check_purchase_offer_user_balance(offer_id: int) -> int:
    """Return the quantity of money that user has right now"""

    offer = get_offer_by_id(offer_id=offer_id)
    user = offer.user
    user_balance = user.balance.get(currency__code="USD")

    return user_balance.quantity


def get_full_price_of_trade(sell_offer_id: int, quantity: int) -> int:
    """Return full price for creating Trade and correctly changing user's balances"""

    sell_offer = get_offer_by_id(offer_id=sell_offer_id)

    return sell_offer.price * quantity


def change_user_balance_by_id(user_id: int, money_quantity: int) -> None:
    """Change the user's balance by the specified amount"""

    balance = Balance.objects.get(user_id=user_id)
    balance.quantity += money_quantity
    balance.save()


def get_or_create_user_inventory(user_id: int, item_id: int) -> Optional[Inventory]:
    """
    Return inventory instance, which belongs to the user
    If it doesn't exist create new inventory instance
    """

    inventory = Inventory.objects.get_or_create(user_id=user_id, item_id=item_id)[0]
    return inventory


def get_item_id_by_code(item_code: str) -> int:
    """Return item instance by the given code"""

    item = Item.objects.get(code=item_code)
    return item.id


def get_or_create_user_balance(user_id: int, currency_id: int) -> Optional[Balance]:
    """
    Return balance instance, which belongs to the user
    If it doesn't exist create new balance instance
    """

    balance = Balance.objects.get_or_create(user_id=user_id, currency_id=currency_id)[0]
    return balance


def change_user_inventory(user_id: int, item_id: int, quantity: int) -> None:
    """Change user's current quantity of stocks for the specified item"""

    inventory = get_or_create_user_inventory(user_id=user_id, item_id=item_id)
    inventory.quantity += quantity
    inventory.save()


def change_offer_current_quantity(offer_id: int, quantity: int) -> None:
    """Change offer's current quantity by the specified amount"""

    offer = get_offer_by_id(offer_id=offer_id)
    offer.quantity += quantity
    offer.save()


def create_trade(
    sell_offer_id: int,
    purchase_offer_id: int,
    quantity: int,
):
    """Create Trade instance with given parameters"""

    sell_offer = get_offer_by_id(offer_id=sell_offer_id)
    purchase_offer = get_offer_by_id(offer_id=purchase_offer_id)
    seller = sell_offer.user
    buyer = purchase_offer.user
    item = sell_offer.item
    description = f"Trade between {seller.username} and {buyer.username}"

    Trade.objects.create(
        item=item,
        seller=seller,
        buyer=buyer,
        quantity=quantity,
        unit_price=sell_offer.price,
        description=description,
        seller_offer=sell_offer,
        buyer_offer=purchase_offer,
    )
