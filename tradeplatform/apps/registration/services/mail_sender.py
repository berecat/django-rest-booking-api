from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.registration.services.db_interaction import get_user_by_email
from apps.registration.tokens import get_user_token
from apps.trades.services.db_interaction import get_user_by_id


def send_mail_message(
    template: str, mail_subject: str, user_id=None, user_email=None
) -> None:
    """Send mail to users with the given template, mail_subjects and to the given user"""

    if user_id:
        user = get_user_by_id(user_id=user_id)
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
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
