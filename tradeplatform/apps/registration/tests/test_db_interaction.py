from django.contrib.auth.models import User

from apps.registration.services.db_interaction import (
    _get_available_quantity_stocks, change_is_active_all_offers_belong_to_user,
    change_offer_is_active, change_profile_valid_by_id, change_user_email,
    check_email_user_exist, get_offer_by_id, get_user_by_email, get_user_by_id,
    get_user_by_username, reset_user_password)
from apps.trades.models import Offer


def test_get_user_by_id(user_instance):
    """Ensure that function return right user instance by the given id"""

    user_id = user_instance.id
    user = get_user_by_id(user_id=user_id)

    assert user == user_instance


def test_get_user_by_email(user_instance):
    """Ensure that function return right user instance by the given email address"""

    email = user_instance.email
    user = get_user_by_email(email=email)

    assert user == user_instance


def test_get_user_by_username(user_instance):
    """Ensure that function return right user instance by the given username"""

    username = user_instance.username
    user = get_user_by_username(username=username)

    assert user == user_instance


def test_change_profile_valid_with_true_by_id(user_instance):
    """Ensure that function confirm user's profile in the right way"""

    change_profile_valid_by_id(user_id=user_instance.id, value=True)

    assert User.objects.get().profile.is_valid


def test_change_profile_valid_with_false_by_id(user_instance):
    """Ensure that function confirm user's profile in the right way"""

    user_instance.profile.is_valid = True
    user_instance.profile.save()

    change_profile_valid_by_id(user_id=user_instance.id, value=False)

    assert not User.objects.get().profile.is_valid


def test_reset_user_password(user_instance):
    """Ensure that function correctly reset user's password"""

    password = "testuserpassword123456"
    reset_user_password(user_id=user_instance.id, password=password)

    assert User.objects.get().check_password(raw_password=password)


def test_change_user_email(user_instance):
    """Ensure that function correctly change user's email address"""

    email = "testuser@email.com"
    change_user_email(user_id=user_instance.id, email=email)

    assert User.objects.get().email == email


def test_check_email_user_exist_with_exist_user(user_instance):
    """Ensure that function return right response with the given email address"""

    result = check_email_user_exist(email=user_instance.email)

    assert result


def test_check_email_user_exist_with_not_exist_user():
    """Ensure that function return right response with the given email address"""

    result = check_email_user_exist(email="fsdfsdfsdfsdf@email.com")

    assert not result


def test_get_offer_by_id(offer_instance):
    """Ensure that function return correct offer instance by the given offer id"""

    offer = get_offer_by_id(offer_id=offer_instance.id)

    assert offer == offer_instance


def test_change_offer_is_active_to_false(offer_instance):
    """
    Ensure that function correctly change offer's is_active attribute
    Since function received False as value, it has to change is_active to False
    """

    offer_instance.is_active = True
    offer_instance.save()

    change_offer_is_active(offer_id=offer_instance.id, value=False)

    assert not Offer.objects.get().is_active


def test_change_offer_is_active_to_true(offer_instance):
    """
    Ensure that function correctly change offer's is_active attribute
    Since function received True as value, it has to change is_active to True
    """

    offer_instance.is_active = False
    offer_instance.save()

    change_offer_is_active(offer_id=offer_instance.id, value=True)

    assert Offer.objects.get().is_active


def test_change_is_active_all_offers_belong_to_user_to_false(offer_instances):
    """Ensure that function correctly change offer's is_active attribute, belongs to the given user"""

    user_id = offer_instances[0].user.id

    change_is_active_all_offers_belong_to_user(user_id=user_id, value=False)

    assert Offer.objects.active().count() == 0


def test_change_is_active_all_offers_belong_to_user_to_true(offer_instances):
    """Ensure that function correctly change offer's is_active attribute, belongs to the given user"""

    user_id = offer_instances[0].user.id

    change_is_active_all_offers_belong_to_user(user_id=user_id, value=True)

    assert Offer.objects.active().count() == 4


def test_get_available_quantity_stocks(offer_purchase_instance):
    """
    Ensure that function return correct quantity of available stocks for now
    In purchase offer instance without current quantity
    """

    available_stocks = _get_available_quantity_stocks(
        offer_id=offer_purchase_instance.id
    )

    assert available_stocks == 60


def test_get_available_quantity_stocks_with_current_quantity(offer_sell_instance):
    """
    Ensure that function return correct quantity of available stocks for now
    In sell offer instance with current quantity
    """

    available_stocks = _get_available_quantity_stocks(offer_id=offer_sell_instance.id)

    assert available_stocks == 36
