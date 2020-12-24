import pytest
from apps.trades.models import Currency, Item, Offer
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture()
def user_instance():
    return mixer.blend(User)


@pytest.fixture()
def item_instance():
    return mixer.blend(Item)


@pytest.fixture()
def default_currency_instance():
    return mixer.blend(Currency, code="USD", name="American dollar")


@pytest.fixture()
def currency_instance():
    return mixer.blend(Currency)


@pytest.fixture()
def offer_purchase_instance(user_instance, item_instance):
    return mixer.blend(Offer, status="PURCHASE", user=user_instance, item=item_instance)


@pytest.fixture()
def offer_sell_instance(user_instance, item_instance):
    return mixer.blend(Offer, status="SELL", user=user_instance, item=item_instance)
