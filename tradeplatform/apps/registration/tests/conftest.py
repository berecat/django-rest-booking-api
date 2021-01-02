import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Function for enable db access for pytest"""

    pass


@pytest.fixture()
def user_instance():
    """User instance"""

    return mixer.blend(User)
