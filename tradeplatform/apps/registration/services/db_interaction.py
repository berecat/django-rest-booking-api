from typing import Optional

from django.contrib.auth.models import User


def get_user_by_id(user_id: int) -> Optional[User]:
    """Return user by id"""

    return User.objects.get(id=user_id)


def get_user_by_email(email: str) -> Optional[User]:
    """Return user instance by the given email"""

    user = User.objects.get(email=email)

    return user


def change_profile_valid_by_id(user_id: int) -> None:
    """Change user profile is_valid attribute"""

    user = get_user_by_id(user_id=user_id)
    user_profile = user.profile

    user_profile.is_valid = True
    user_profile.save()
