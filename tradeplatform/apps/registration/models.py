from apps.trades.models import Balance, WatchList
from apps.trades.services.db_interaction import get_or_create_default_currency
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Class that represent user's profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_valid = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def create_user_default_attributes(sender, instance, created, **kwargs):
    """Function create necessary attributes for user after created him"""

    if created:
        UserProfile.objects.create(user=instance)
        Balance.objects.create(user=instance, currency=get_or_create_default_currency())
        WatchList.objects.create(user=instance)
