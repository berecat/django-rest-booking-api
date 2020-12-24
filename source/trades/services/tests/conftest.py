import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from trades.models import Item, Offer


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope="function")
def user_instance():
    return mixer.blend(User)


@pytest.fixture(scope="function")
def item_instance():
    return mixer.blend(Item)


@pytest.fixture(scope="function")
def offer_purchase_instance(user_instance, item_instance):
    return mixer.blend(Offer, status="PURCHASE", user=user_instance, item=item_instance)


@pytest.fixture(scope="function")
def offer_sell_instance(user_instance, item_instance):
    return mixer.blend(Offer, status="SELL", user=user_instance, item=item_instance)
