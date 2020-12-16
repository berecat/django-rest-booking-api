from django.db import models
from django.contrib.auth.models import User


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
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)
    details = models.TextField("Details", blank=True, null=True, max_length=512)


class Price(models.Model):
    """Item prices"""
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE, related_name='prices',
                             related_query_name='prices', )
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(unique=True, blank=True, null=True)


class BaseUserItem(models.Model):
    """Base for models that have user and item attributes"""
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class WatchList(BaseUserItem):
    """Current user, favorite list of stocks"""


class Offer(BaseUserItem):
    """Request to buy or sell specific stocks"""
    entry_quantity = models.IntegerField("Requested quantity")
    quantity = models.IntegerField("Current quantity")
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Inventory(BaseUserItem):
    """The number of stocks in particular user has"""
    quantity = models.IntegerField("Stocks quantity", default=0)


class Trade(models.Model):
    """Information about s certain transaction"""
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='seller_trade',
        related_query_name='seller_trade',
    )
    buyer = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buyer_trade',
        related_query_name='buyer_trade',
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    buyer_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buyer_trade',
        related_query_name='buyer_trade',
    )
    seller_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='seller_trade',
        related_query_name='seller_trade',
    )