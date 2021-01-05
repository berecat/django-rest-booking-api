from django.contrib.auth.models import User

from apps.registration.services.tokens import (
    confirm_user_email_by_given_token,
    get_user_id_by_given_token,
    get_user_token,
    validate_given_user_token,
)


def test_validate_given_user_token_with_right_token(user_instance):
    """
    Ensure that function return right response after checking user token
    Since token is right for the given user, function has to return True
    """

    token = get_user_token(user_id=user_instance.id)
    result = validate_given_user_token(token=token)

    assert result


def test_validate_given_user_token_with_wrong_token(user_instance):
    """
    Ensure that function return right response after checking user token
    Since token is wrong for the given user, function has to return False
    """

    token = get_user_token(user_id=user_instance.id)[:-3]
    result = validate_given_user_token(token=token)

    assert not result


def test_get_user_id_by_given_token_with_right_token(user_instance):
    """Ensure that function return right user's id by the given token"""

    token = get_user_token(user_id=user_instance.id)
    user_id = get_user_id_by_given_token(token=token)

    assert user_id == user_instance.id


def test_get_user_id_by_given_token_with_wrong_token(user_instance):
    """Ensure that function return right user's id by the given token"""

    token = get_user_token(user_id=user_instance.id)[:-5]
    user_id = get_user_id_by_given_token(token=token)

    assert user_id is None


def test_confirm_user_email_by_given_token(user_instance):
    """Ensure that function correctly change user's profile is_valid attribute"""

    token = get_user_token(user_id=user_instance.id)
    confirm_user_email_by_given_token(token=token)

    assert User.objects.get().profile.is_valid
