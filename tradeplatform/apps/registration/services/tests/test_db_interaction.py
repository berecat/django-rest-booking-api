from apps.registration.services.db_interaction import (
    change_profile_valid_by_id, get_user_by_email, get_user_by_id)


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


def test_change_profile_valid_by_id(user_instance):
    """Ensure that function confirm user's profile in the right way"""

    print(user_instance.profile.is_valid)
    change_profile_valid_by_id(user_id=user_instance.id)

    assert user_instance.profile.is_valid == True
