from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def send_confirmation_mail_message(sender, **kwargs):
    """Function send confirmation mail message for user, who has just registered"""
