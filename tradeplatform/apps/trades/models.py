from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class StockBase(models.Model):
    """Base for models that have code and name attributes"""

    code = models.CharField("Code", max_length=8, unique=True)
    name = models.CharField("Name", max_length=24, unique=True)

    class Meta:
        abstract = True


class Currency(StockBase):
    """Currency"""

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


class Item(StockBase):
    """Particular stock"""

    details = models.TextField("Details", blank=True, null=True, max_length=512)

    def __str__(self):
        return f"{self.code} : {self.name}"


class Price(models.Model):
    """Item prices"""

    currency = models.ForeignKey(
        Currency,
        default=1,
        on_delete=models.SET_DEFAULT,
        related_name="+",
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="price",
        related_query_name="price",
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(blank=True, null=True)


class WatchList(models.Model):
    """Current user, favorite list of stocks"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="watchlist",
    )
    item = models.ManyToManyField(Item, blank=True, related_name="+")


class BaseUserItem(models.Model):
    """Base for models that have user and item attributes"""

    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class StatusChoices(Enum):
    """Enum class, which gives choices for status attribute in Offer model"""

    PURCHASE = "PURCHASE"
    SELL = "SELL"

    @classmethod
    def choices(cls):
        """
        :return: status choices as tuple of tuples
        the first value - value of attribute, the second value - it's string representation
        """

        return tuple((i.name, i.value) for i in cls)


class OfferManager(models.Manager):
    """Queryset manager for Offer model"""

    def active(self):
        """
        :return: all Offer's instance that are active
        """

        return self.get_queryset().filter(is_active=True)

    def sell_offers(self):
        """
        :return: all Offer's instance that are active and have sell status
        """

        return self.get_queryset().filter(status="SELL", is_active=True)

    def purchase_offers(self):
        """
        :return: all Offer's instance that are active and have purchase status
        """

        return self.get_queryset().filter(status="PURCHASE", is_active=True)


class Offer(BaseUserItem):
    """Request to buy or sell specific stocks"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="offer",
        related_query_name="offer",
    )
    status = models.CharField(max_length=8, choices=StatusChoices.choices())
    entry_quantity = models.IntegerField("Requested quantity")
    quantity = models.IntegerField("Current quantity", default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_active = models.BooleanField(default=True)

    objects = OfferManager()

    def __str__(self):
        return f"{self.status} - {self.price} - {self.user} - {self.item}"


class Inventory(BaseUserItem):
    """The number of stocks in particular user has"""

    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="inventory",
        related_query_name="inventory",
    )
    quantity = models.PositiveIntegerField("Stocks quantity", default=1000)

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"


class Balance(models.Model):
    """The number of money in particular user has"""

    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="balance",
        related_query_name="balance",
    )
    currency = models.ForeignKey(
        Currency,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    quantity = models.PositiveIntegerField("Money quantity", default=1000)


class Trade(models.Model):
    """Information about s certain transaction"""

    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="seller_trade",
        related_query_name="seller_trade",
    )
    buyer = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="buyer_trade",
        related_query_name="buyer_trade",
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    buyer_offer = models.ForeignKey(
        Offer,
        null=True,
        on_delete=models.SET_NULL,
        related_name="buyer_trade",
        related_query_name="buyer_trade",
    )
    seller_offer = models.ForeignKey(
        Offer,
        null=True,
        on_delete=models.SET_NULL,
        related_name="seller_trade",
        related_query_name="seller_trade",
    )
    date = models.DateTimeField(auto_now_add=True)
