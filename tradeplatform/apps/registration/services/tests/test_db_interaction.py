from django.contrib.auth.models import User

from apps.registration.services.db_interaction import (
    change_profile_valid_by_id, change_user_email, get_user_by_email,
    get_user_by_id, reset_user_password)


def test_get_user_by_id(user_instance):
    """Ensure that function return right user instance"""

    user_id = user_instance.id
    user = get_user_by_id(user_id=user_id)

    assert user == user_instance


def test_get_user_by_email(user_instance):
    """Ensure that function return right user instance"""

    email = user_instance.email
    user = get_user_by_email(email=email)

    assert user == user_instance


def test_change_profile_valid_with_true_by_id(user_instance):
    """Ensure that function confirm user's profile in the right way"""

    change_profile_valid_by_id(user_id=user_instance.id, value=True)

    assert User.objects.get().profile.is_valid == True


def test_change_profile_valid_with_false_by_id(user_instance):
    """Ensure that function confirm user's profile in the right way"""

    user_instance.profile.is_valid = True
    user_instance.profile.save()

    change_profile_valid_by_id(user_id=user_instance.id, value=False)

    assert User.objects.get().profile.is_valid == False


def test_reset_user_password(user_instance):
    """Ensure that function correctly reset user's password"""

    password = "testuserpassword123456"
    reset_user_password(user_id=user_instance.id, password=password)

    assert User.objects.get().check_password(raw_password=password) == True


def test_change_user_email(user_instance):
    """Ensure that function correctly change user's email address"""

    email = "testuser@email.com"
    change_user_email(user_id=user_instance.id, email=email)

    assert User.objects.get().email == email
