from celery import shared_task

from apps.registration.services.mail_sender import send_mail_message
from apps.registration.services.views_logic import update_user_email_address


@shared_task
def send_confirmation_mail_message(username: str) -> None:
    """Send mail message to users for confirmation them email address"""

    send_mail_message(
        template="registration/acc_active_email.html",
        mail_subject="Activate your API account",
        username=username,
    )


@shared_task
def send_reset_password_mail(email: str) -> None:
    """Send mail to users for changing their password"""

    send_mail_message(
        template="registration/reset_password.html",
        mail_subject="Confirm your password change request",
        user_email=email,
    )


@shared_task
def send_change_email_address_mail(username: str) -> None:
    """Send mail to users for changing their email address"""

    send_mail_message(
        template="registration/change_email.html",
        mail_subject="Confirm your email address change request",
        username=username,
    )


@shared_task
def change_email_address(username: str, to_email: str, token: str) -> None:
    """Send mail to users to confirm new email address"""

    send_mail_message(
        template="registration/confirm_change_email.html",
        mail_subject="Confirm your new email address",
        username=username,
        to_email=to_email,
    )
    update_user_email_address(token="token", email=to_email)
