from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.registration.tasks import send_confirmation_mail_message
from apps.trades.models import Balance, WatchList
from apps.trades.services.db_interaction import get_or_create_default_currency


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


@receiver(post_save, sender=User)
def send_confirmation_email_to_user(sender, instance, created, **kwargs):
    """Function send confirmation mail message for user, who has just registered"""

    if created:
        send_confirmation_mail_message.delay(user_id=instance.id)
