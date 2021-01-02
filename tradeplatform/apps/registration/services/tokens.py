from typing import Optional

from apps.registration.services.db_interaction import (
    change_profile_valid_by_id, get_user_by_id)
from django.contrib.auth.models import User
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken


def validate_given_user_token(token: str) -> bool:
    """
    Check that token is valid. If token is valid change
    user's profile attribute is valid to True
    """

    user_id = get_user_id_by_given_token(token=token)

    try:
        User.objects.get(id=user_id)
        return True
    except User.DoesNotExist:
        return False


def get_user_token(user_id: int) -> str:
    """Get user's JWT token"""

    user = get_user_by_id(user_id=user_id)
    token = AccessToken.for_user(user=user)

    return str(token)


def get_user_id_by_given_token(token: str) -> Optional[int]:
    """Get user id by the given token"""

    try:
        user_id = AccessToken(token=token, verify=True).get("user_id")
        return user_id
    except TokenError:
        return None


def confirm_user_email_by_given_token(token: str) -> None:
    """Change user profile is_valid by given token"""

    user_id = get_user_id_by_given_token(token=token)
    change_profile_valid_by_id(user_id=user_id, value=True)
