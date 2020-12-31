from typing import Optional

from django.contrib.auth.models import User

from apps.trades.services.db_interaction import get_user_by_id


def get_user_by_email(email: str) -> Optional[User]:
    """Return user instance by the given email"""

    user = User.objects.get(email=email)

    return user


def change_user_profile_valid_by_id(user_id: int) -> None:
    """Change user profile is_valid attribute"""

    user = get_user_by_id(user_id=user_id)
    user_profile = user.profile

    user_profile.is_valid = not user_profile.is_valid
    user_profile.save()
