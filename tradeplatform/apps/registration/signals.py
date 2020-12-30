from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.registration.models import UserProfile


@receiver(post_save, sender=User)
def send_confirmation_mail_message(sender, instance, created, **kwargs):
    """Function send confirmation mail message for user, who has just registered"""

    if created:
        UserProfile.objects.create(user=instance)
