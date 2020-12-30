from django.apps import AppConfig


class RegistrationConfig(AppConfig):
    name = "registration"

    def ready(self):
        from django.contrib.auth.models import User
        from django.db.models.signals import post_save
        from apps.registration.signals import send_confirmation_mail_message

        post_save.connect(send_confirmation_mail_message, sender=User)
