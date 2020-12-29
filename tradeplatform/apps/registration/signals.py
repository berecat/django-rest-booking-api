from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def send_confirmation_mail_message(sender, instance, **kwargs):
    """Function send confirmation mail message for user, who has just registered"""

