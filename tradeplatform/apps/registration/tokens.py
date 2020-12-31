from typing import Optional

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.trades.services.db_interaction import get_user_by_id, change_user_profile_valid_by_id


def check_token(token: str) -> bool:
    """
    Check that token is valid. If token is valid change
    user's profile attribute is valid to True
    """

    user_id = _get_user_id_by_given_token(token=token)
    user = User.objects.get(id=user_id)

    if user:
        change_user_profile_valid_by_id(user_id=user_id)
        return True
    return False


def get_user_token(user_id: int) -> str:
    """Get user's JWT token"""

    user = get_user_by_id(user_id=user_id)
    token = AccessToken.for_user(user=user)

    return str(token)


def _get_user_id_by_given_token(token: str) -> Optional[int]:
    """Get user id by the given token"""

    try:
        user_id = AccessToken(token=token, verify=True).get("user_id")
        return user_id
    except TokenError:
        return
