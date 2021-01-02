from django.contrib.auth.models import User

from apps.registration.services.tokens import get_user_token
from apps.registration.services.views_logic import (update_user_email_address,
                                                    update_user_password)


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
