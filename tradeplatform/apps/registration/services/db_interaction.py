from typing import Optional

from django.contrib.auth.models import User

from apps.trades.models import Offer


def get_user_by_id(user_id: int) -> Optional[User]:
    """Return user by id"""

    return User.objects.get(id=user_id)


def get_user_by_email(email: str) -> Optional[User]:
    """Return user instance by the given email"""

    user = User.objects.get(email=email)

    return user


def get_user_by_username(username: str) -> Optional[User]:
    """Return user instance by the given username"""

    user = User.objects.get(username=username)

    return user


def change_profile_valid_by_id(user_id: int, value: bool) -> None:
    """Change user profile is_valid attribute"""

    user = get_user_by_id(user_id=user_id)
    user_profile = user.profile

    user_profile.is_valid = value
    user_profile.save()


def reset_user_password(user_id: int, password: str) -> None:
    """Reset user password by the given JWT token"""

    user = get_user_by_id(user_id=user_id)
    user.set_password(password)
    user.save()


def change_user_email(user_id: int, email: str) -> None:
    """Change user's email address"""

    user = get_user_by_id(user_id=user_id)
    user.email = email
    user.save()


def check_email_user_exist(email: str) -> bool:
    """Check that user with the given email exist"""

    try:
        User.objects.get(email=email)
        return True
    except User.DoesNotExist:
        return False


def get_offer_by_id(offer_id: int) -> Optional[Offer]:
    """Return offer instance by the given id"""

    offer = Offer.objects.get(id=offer_id)
    return offer


def change_offer_is_active(offer_id: int, value: bool) -> None:
    """Change offer's is_active attribute to the given value"""

    offer = get_offer_by_id(offer_id=offer_id)
    offer.is_active = value
    offer.save()


def change_is_active_all_offers_belong_to_user(user_id: int, value: bool) -> None:
    """Change all offer's is_active attribute, which belongs to the given user"""

    for offer in Offer.objects.all().filter(user__id=user_id):
        change_offer_is_active(offer_id=offer.id, value=value)
