from apps.registration.services.db_interaction import (
    change_is_active_all_offers_belong_to_user, change_profile_valid_by_id,
    change_user_email, reset_user_password)
from apps.registration.services.tokens import get_user_id_by_given_token


def update_user_password(token: str, password: str) -> None:
    """Function reset user password by the given token and password"""

    user_id = get_user_id_by_given_token(token=token)

    reset_user_password(user_id=user_id, password=password)


def update_user_email_address(token: str, email: str) -> None:
    """
    Function change user email address and reset is_valid attribute in profile to False
    by the given token and email
    """

    user_id = get_user_id_by_given_token(token=token)

    change_profile_valid_by_id(user_id=user_id, value=False)
    change_user_email(user_id=user_id, email=email)


def change_user_offer_after_changing_email(token: str, value: bool) -> None:
    """Function change all user's offer is_active attribute to the given value"""

    user_id = get_user_id_by_given_token(token=token)

    change_is_active_all_offers_belong_to_user(user_id=user_id, value=value)
