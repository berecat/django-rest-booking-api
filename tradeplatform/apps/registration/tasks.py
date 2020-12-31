from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.trades.services.db_interaction import get_user_by_id
from apps.registration.tokens import get_user_token


@shared_task
def send_confirmation_mail_message(user_id: int):
    user = get_user_by_id(user_id=user_id)
    mail_subject = "Activate your blog account."
    message = render_to_string(
        "registration/acc_active_email.html",
        {
            "user": user,
            "domain": "0.0.0.0:8000",
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": get_user_token(user_id=user_id),
        },
    )
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
