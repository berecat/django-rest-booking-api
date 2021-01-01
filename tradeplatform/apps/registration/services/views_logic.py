from apps.registration.services.db_interaction import (
    change_profile_valid_by_id, change_user_email, reset_user_password)
from apps.registration.tokens import get_user_id_by_given_token


def update_user_password(token: str, password: str) -> None:
    """"""

    user_id = get_user_id_by_given_token(token=token)

    reset_user_password(user_id=user_id, password=password)


def update_user_email_address(token: str, email: str) -> None:
    """"""

    user_id = get_user_id_by_given_token(token=token)

    change_profile_valid_by_id(user_id=user_id, value=False)
    change_user_email(user_id=user_id, email=email)
