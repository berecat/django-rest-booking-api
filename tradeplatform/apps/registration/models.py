from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.trades.models import Balance, WatchList
from apps.trades.services.db_interaction import get_or_create_default_currency


class UserProfile(models.Model):
    """Class that represent user's profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_valid = models.BooleanField(default=False)
    information = models.TextField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    @property
    def count_all_trades(self):
        """Count all trades, which user has made"""

        return self.user.buyer_trade.count() + self.user.seller_trade.count()

    @property
    def count_buy_money(self):
        """The amount of money that the user spent to trades"""

        quantity_money = 0
        for trade in self.user.buyer_trade.all():
            quantity_money += trade.unit_price * trade.quantity

        return quantity_money

    @property
    def count_sell_money(self):
        """The amount of money that the user received from trades"""

        quantity_money = 0
        for trade in self.user.seller_trade.all():
            quantity_money += trade.unit_price * trade.quantity

        return quantity_money


@receiver(post_save, sender=User)
def create_user_default_attributes(sender, instance, created, **kwargs):
    """Function create necessary attributes for user after created him"""

    if created:
        UserProfile.objects.create(user=instance)
        Balance.objects.create(user=instance, currency=get_or_create_default_currency())
        WatchList.objects.create(user=instance)
