from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.registration.services.db_interaction import (get_user_by_email,
                                                       get_user_by_username)
from apps.registration.tokens import get_user_token


def send_mail_message(
    template: str,
    mail_subject: str,
    username: str = None,
    user_email: str = None,
    to_email: str = None,
) -> None:
    """Send mail to users with the given template, mail_subjects and to the given user"""

    if username:
        user = get_user_by_username(username=username)
    else:
        user = get_user_by_email(email=user_email)

    message = render_to_string(
        template,
        {
            "user": user,
            "domain": "0.0.0.0:8000",
            "token": get_user_token(user_id=user.id),
        },
    )

    if not to_email:
        to_email = user.email

    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
