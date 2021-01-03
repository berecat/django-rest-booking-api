import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer

from apps.trades.models import Offer


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Function for enable db access for pytest"""

    pass


@pytest.fixture()
def user_instance():
    """User instance"""

    return mixer.blend(User)


@pytest.fixture()
def offer_instance():
    """Offer instance"""

    return mixer.blend(Offer)


@pytest.fixture()
def offer_instances(user_instance):
    """Offer instances"""

    return [
        mixer.blend(Offer, user=user_instance, is_active=True),
        mixer.blend(Offer, user=user_instance, is_active=False),
        mixer.blend(Offer, user=user_instance, is_active=False),
        mixer.blend(Offer, user=user_instance, is_active=True),
    ]
