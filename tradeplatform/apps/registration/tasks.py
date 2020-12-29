from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.registration.tokens import account_activation_token
from apps.trades.services.db_interaction import get_user_by_id


@shared_task
def send_confirmation_mail_message(user_id: int, domain: str):
    user = get_user_by_id(user_id=user_id)
    mail_subject = "Activate your blog account."
    message = render_to_string(
        "acc_active_email.html",
        {
            "user": user,
            "domain": domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()