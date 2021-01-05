from django.contrib.auth.models import User

from apps.registration.services.tokens import get_user_token
from apps.registration.services.views_logic import (
    change_user_offer_after_changing_email,
    update_user_email_address,
    update_user_password,
)
from apps.trades.models import Offer


def test_update_user_password_with_right_token(user_instance):
    """Ensure that function correctly update user's password"""

    password = "testuserpassword"
    token = get_user_token(user_id=user_instance.id)
    update_user_password(token=token, password=password)

    assert User.objects.get().check_password(raw_password=password) == True


def test_update_user_email_address(user_instance):
    """Ensure that function correctly update user's email address"""

    email = "testuser@gmail.com"
    token = get_user_token(user_id=user_instance.id)
    update_user_email_address(token=token, email=email)

    assert User.objects.get().email == email


def test_change_user_offer_after_changing_email_to_true(offer_instances):
    """Ensure that function correctly change all user's offer's attribute is_active to True"""

    token = get_user_token(user_id=offer_instances[0].user.id)
    change_user_offer_after_changing_email(token=token, value=True)

    assert Offer.objects.active().count() == 4


def test_change_user_offer_after_changing_email_to_false(offer_instances):
    """Ensure that function correctly change all user's offer's attribute is_active to False"""

    token = get_user_token(user_id=offer_instances[0].user.id)
    change_user_offer_after_changing_email(token=token, value=False)

    assert Offer.objects.active().count() == 0
