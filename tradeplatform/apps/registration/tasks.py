from celery import shared_task

from apps.registration.services.mail_sender import send_mail_message


@shared_task
def send_confirmation_mail_message(user_id: int):
    """Send mail message to users for confirmation them email address"""

    send_mail_message(
        template="registration/acc_active_email.html",
        mail_subject="Activate your API account",
        user_id=user_id,
    )


@shared_task
def send_reset_password_mail(email: str):
    """Send mail to users for changing their password"""

    send_mail_message(
        template="registration/reset_password.html",
        mail_subject="Confirm your password change request",
        user_email=email,
    )
