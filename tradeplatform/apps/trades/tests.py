from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.trades.models import (Balance, Currency, Inventory, Item, Offer,
                                Price, Trade, WatchList)


class TestCurrency(APITestCase):
    """Test class for Currency model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        User.objects.create_user(
            username="test_user",
            password="test",
        )
        self.client.login(username="test_user", password="test")

    def post_currency(self, data):
        """Post currency instance into database through web-api"""

        url = reverse("currency-list")
        response = self.client.post(url, data, format="json")
        return response

    def test_currency_post(self):
        """
        Ensure we can post currency instance
        """

        data = {"code": "USD", "name": "American Dollar"}
        response = self.post_currency(data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Currency.objects.count() == 1
        assert Currency.objects.get().name == data["name"]
        assert Currency.objects.get().code == data["code"]

    def test_currencies_list(self):
        """
        Ensure we can retrieve the currencies collection
        """

        data_currency_1 = {
            "code": "USD",
            "name": "American Dollar",
        }
        self.post_currency(data_currency_1)

        data_currency_2 = {
            "code": "EUR",
            "name": "Euro",
        }
        self.post_currency(data_currency_2)

        url = reverse("currency-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        assert response.data["results"][0]["name"] == data_currency_1["name"]
        assert response.data["results"][0]["code"] == data_currency_1["code"]
        assert response.data["results"][1]["name"] == data_currency_2["name"]
        assert response.data["results"][1]["code"] == data_currency_2["code"]

    def test_currency_get(self):
        """
        Ensure we can get a single currency by id
        """

        data = {"code": "USD", "name": "American Dollar"}
        response = self.post_currency(data)

        url = reverse("currency-detail", None, {response.data["id"]})
        get_response = self.client.get(url, format="json")

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data["name"] == data["name"]
        assert get_response.data["code"] == data["code"]

    def test_currency_patch_update(self):
        """
        Ensure we can update fields for a currency by patch method
        """

        data = {"code": "BYN", "name": "American Dollar"}
        response = self.post_currency(data)

        url = reverse("currency-detail", None, {response.data["id"]})
        new_data = {
            "code": "USD",
        }
        patch_response = self.client.patch(url, new_data, format="json")

        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data["name"] == data["name"]
        assert patch_response.data["code"] == new_data["code"]

    def test_currency_put_update(self):
        """
        Ensure we can update fields for a currency by put method
        """

        data = {"code": "USD", "name": "American Dollar"}
        response = self.post_currency(data)

        url = reverse("currency-detail", None, {response.data["id"]})
        new_data = {
            "code": "EUR",
            "name": "EURO",
        }
        put_response = self.client.put(url, new_data, format="json")

        assert put_response.status_code == status.HTTP_200_OK
        assert put_response.data["name"] == new_data["name"]
        assert put_response.data["code"] == new_data["code"]


class TestItem(APITestCase):
    """Test class for Item model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        User.objects.create_user(username="test_user", password="test")
        self.client.login(username="test_user", password="test")

    def post_item(self, data):
        """Post item instance into database through web-api"""

        url = reverse("item-list")
        response = self.client.post(url, data, format="json")
        return response

    def test_item_post(self):
        """
        Ensure we can post item instance
        """

        data = {"code": "AAPL", "name": "Apple", "details": "Stocks of Apple Inc."}
        response = self.post_item(data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Item.objects.count() == 1
        assert Item.objects.get().name == data["name"]
        assert Item.objects.get().code == data["code"]
        assert Item.objects.get().details == data["details"]

    def test_items_list(self):
        """
        Ensure we can retrieve the items collection
        """

        data_item_1 = {
            "code": "AAPL",
            "name": "Apple",
            "details": "Stocks of Apple Inc.",
        }
        self.post_item(data_item_1)

        data_item_2 = {
            "code": "TSLA",
            "name": "Tesla",
            "details": "Stocks of Tesla Inc.",
        }
        self.post_item(data_item_2)

        url = reverse("item-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        assert response.data["results"][0]["name"] == data_item_1["name"]
        assert response.data["results"][0]["code"] == data_item_1["code"]
        assert response.data["results"][0]["details"] == data_item_1["details"]
        assert response.data["results"][1]["name"] == data_item_2["name"]
        assert response.data["results"][1]["code"] == data_item_2["code"]
        assert response.data["results"][1]["details"] == data_item_2["details"]

    def test_item_get(self):
        """
        Ensure we can get a single item by id
        """

        data = {
            "code": "TSLA",
            "name": "Tesla",
            "details": "Stocks of Tesla Inc.",
        }
        response = self.post_item(data)

        url = reverse("item-detail", None, {response.data["id"]})
        get_response = self.client.get(url, format="json")

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data["name"] == data["name"]
        assert get_response.data["code"] == data["code"]
        assert get_response.data["details"] == data["details"]

    def test_item_patch_update(self):
        """
        Ensure we can update fields for a item by patch method
        """

        data = {
            "code": "TSLA",
            "name": "Tesla",
            "details": "Stocks of Tesla Inc.",
        }
        response = self.post_item(data)

        url = reverse("item-detail", None, {response.data["id"]})
        new_data = {
            "code": "AAPL",
            "details": "Stocks of Apple Inc.",
        }
        patch_response = self.client.patch(url, new_data, format="json")

        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data["name"] == data["name"]
        assert patch_response.data["code"] == new_data["code"]
        assert patch_response.data["details"] == new_data["details"]

    def test_item_put_update(self):
        """
        Ensure we can update fields for a item by put method
        """

        data = {
            "code": "TSLA",
            "name": "Tesla",
            "details": "Stocks of Tesla Inc.",
        }
        response = self.post_item(data)

        url = reverse("item-detail", None, {response.data["id"]})
        new_data = {
            "code": "AAPL",
            "name": "Apple",
            "details": "Stocks of Apple Inc.",
        }
        put_response = self.client.put(url, new_data, format="json")

        assert put_response.status_code == status.HTTP_200_OK
        assert put_response.data["name"] == new_data["name"]
        assert put_response.data["code"] == new_data["code"]
        assert put_response.data["details"] == new_data["details"]

    def test_item_delete(self):
        """
        Ensure we can delete a single item instance
        """

        data = {
            "code": "TSLA",
            "name": "Tesla",
            "details": "Stocks of Tesla Inc.",
        }
        response = self.post_item(data)

        url = reverse("item-detail", None, {response.data["id"]})
        delete_response = self.client.delete(url, format="json")

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        assert Item.objects.count() == 0


class TestPrice(APITestCase):
    """Test class for Price model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        User.objects.create_user(username="test_user", password="test")
        self.client.login(username="test_user", password="test")

        self.currency_1 = Currency.objects.create(code="USD", name="American Dollar")
        self.currency_2 = Currency.objects.create(code="EUR", name="Euro")

        self.item_1 = Item.objects.create(
            code="AAPL", name="Apple", details="Stocks of Apple Inc."
        )
        self.item_2 = Item.objects.create(
            code="AMZN", name="Amazon", details="Stocks of Amazon"
        )

    def post_price(self, data):
        """Post price instance into database through web-api"""

        url = reverse("price-list")
        response = self.client.post(url, data, format="json")
        return response

    def test_price_post(self):
        """
        Ensure we can post price instance
        """

        data = {
            "currency": self.currency_1.id,
            "item": self.item_1.id,
            "price": 1242,
            "date": "2020-12-23 10:05:00+00:00",
        }
        response = self.post_price(data)
        print(response)

        assert response.status_code == status.HTTP_201_CREATED
        assert Price.objects.count() == 1
        assert Price.objects.get().currency == self.currency_1
        assert Price.objects.get().item == self.item_1
        assert Price.objects.get().price == data["price"]
        assert Price.objects.get().date.__str__() == data["date"]

    def test_prices_list(self):
        """
        Ensure we can retrieve the prices collection
        """

        data_price_1 = {
            "currency": self.currency_1.id,
            "item": self.item_1.id,
            "price": Decimal("12.04"),
            "date": "2020-12-23T10:05:00Z",
        }
        self.post_price(data_price_1)

        data_price_2 = {
            "currency": self.currency_2.id,
            "item": self.item_2.id,
            "price": Decimal("2123.01"),
            "date": "2020-10-14T13:05:00Z",
        }
        self.post_price(data_price_2)

        url = reverse("price-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        assert response.data["results"][0]["currency"]["id"] == data_price_1["currency"]
        assert response.data["results"][0]["item"] == self.item_1.code
        assert response.data["results"][0]["price"] == data_price_1["price"].__str__()
        assert response.data["results"][0]["date"].__str__() == data_price_1["date"]

        assert response.data["results"][1]["currency"]["id"] == data_price_2["currency"]
        assert response.data["results"][1]["item"] == self.item_2.code
        assert response.data["results"][1]["price"] == data_price_2["price"].__str__()
        assert response.data["results"][1]["date"].__str__() == data_price_2["date"]

    def test_price_get(self):
        """
        Ensure we can get a single price by id
        """

        data = {
            "currency": self.currency_2.id,
            "item": self.item_2.id,
            "price": Decimal("2123.01"),
            "date": "2020-10-14T13:05:00Z",
        }
        response = self.post_price(data)

        url = reverse("price-detail", None, {response.data["id"]})
        get_response = self.client.get(url, format="json")

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data["currency"]["id"] == data["currency"]
        assert get_response.data["item"] == self.item_2.code
        assert get_response.data["price"] == data["price"].__str__()
        assert get_response.data["date"].__str__() == data["date"]

    def test_price_patch_update(self):
        """
        Ensure we can update fields for a price by patch method
        """

        data = {
            "currency": self.currency_2.id,
            "item": self.item_2.id,
            "price": Decimal("2123.01"),
            "date": "2020-10-14T13:05:00Z",
        }
        response = self.post_price(data)

        url = reverse("price-detail", None, {response.data["id"]})
        new_data = {
            "currency": self.currency_1.id,
            "item": self.item_1.id,
        }
        patch_response = self.client.patch(url, new_data, format="json")

        print(patch_response.data)

        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data["currency"] == new_data["currency"]
        assert patch_response.data["item"] == new_data["item"]
        assert patch_response.data["price"] == data["price"].__str__()
        assert patch_response.data["date"].__str__() == data["date"]

    def test_price_put_update(self):
        """
        Ensure we can update fields for a price by put method
        """

        data = {
            "currency": self.currency_2.id,
            "item": self.item_2.id,
            "price": Decimal("2123.01"),
            "date": "2020-12-23T10:05:00Z",
        }
        response = self.post_price(data)

        url = reverse("price-detail", None, {response.data["id"]})
        new_data = {
            "currency": self.currency_1.id,
            "item": self.item_1.id,
            "price": Decimal("4234.01"),
            "date": "2020-10-14T13:05:00Z",
        }
        put_response = self.client.put(url, new_data, format="json")

        assert put_response.status_code == status.HTTP_200_OK
        assert put_response.data["currency"] == new_data["currency"]
        assert put_response.data["item"] == new_data["item"]
        assert put_response.data["price"] == new_data["price"].__str__()
        assert put_response.data["date"].__str__() == new_data["date"]

    def test_price_delete(self):
        """
        Ensure we can delete a single price instance
        """

        data = {
            "currency_id": self.currency_2.id,
            "item": self.item_2.id,
            "price": Decimal("2123.01"),
            "date": "2020-12-23T10:05:00Z",
        }
        response = self.post_price(data)

        url = reverse("price-detail", None, {response.data["id"]})
        delete_response = self.client.delete(url, format="json")

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        assert Price.objects.count() == 0

    def test_price_representation_item(self):
        """
        Ensure price's representation in related item model is correct
        """

        data_price_1 = {
            "currency": self.currency_2.id,
            "item": self.item_2.id,
            "price": Decimal("2123.01"),
            "date": "2020-12-23T10:05:00Z",
        }
        price_1 = self.post_price(data_price_1).data

        data_price_2 = {
            "currency": self.currency_1.id,
            "item": self.item_2.id,
            "price": Decimal("2123.01"),
            "date": "2020-12-23T13:05:00Z",
        }
        price_2 = self.post_price(data_price_2).data

        url = reverse("item-detail", None, {self.item_2.id})
        response = self.client.get(url, format="json")

        print(response.data["price"][0])

        assert response.data["price"][0]["id"] == price_1["id"]
        assert response.data["price"][1]["id"] == price_2["id"]


class TestWatchlist(APITestCase):
    """Test class for Watchlist model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        self.user_1 = User.objects.create_user(username="test_user", password="test")
        self.client.login(username="test_user", password="test")

        self.item_1 = Item.objects.create(
            name="Apple",
            code="AAPL",
        )
        self.item_2 = Item.objects.create(
            name="Tesla",
            code="TSLA",
        )
        self.item_3 = Item.objects.create(
            name="Amazon",
            code="AMZN",
        )

    def post_watchlist(self, data):
        """Post watchlist instance into database through web-api"""

        url = reverse("watchlist-list")
        response = self.client.post(url, data, format="json")
        return response

    def test_watchlist_post(self):
        """
        Ensure we can post watchlist instance
        """

        data = {"item": [self.item_1.id, self.item_2.id]}
        response = self.post_watchlist(data)

        print(response.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert WatchList.objects.count() == 1
        assert WatchList.objects.get().user == self.user_1
        assert len(WatchList.objects.get().item.all()) == 2
        assert WatchList.objects.get().item.all()[0] == self.item_1
        assert WatchList.objects.get().item.all()[1] == self.item_2

    def test_watchlists_list(self):
        """
        Ensure we can retrieve the watchlists collection
        """

        data_watchlist_1 = {
            "item": [
                self.item_1.id,
                self.item_2.id,
            ],
        }
        self.post_watchlist(data_watchlist_1)

        url = reverse("watchlist-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

        assert response.data["results"][0]["user"]["username"] == self.user_1.username
        assert len(response.data["results"][0]["item"]) == 2
        assert (
            response.data["results"][0]["item"][0]["id"] == data_watchlist_1["item"][0]
        )
        assert (
            response.data["results"][0]["item"][1]["id"] == data_watchlist_1["item"][1]
        )

    def test_watchlist_get(self):
        """
        Ensure we can get a single watchlist by id
        """

        data = {
            "item": [
                self.item_1.id,
                self.item_2.id,
                self.item_3.id,
            ],
        }
        response = self.post_watchlist(data)

        url = reverse("watchlist-detail", None, {response.data["id"]})
        get_response = self.client.get(url, format="json")
        print(get_response.data)

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data["user"]["username"] == self.user_1.username
        assert len(get_response.data["item"]) == 3
        assert get_response.data["item"][0]["id"] == data["item"][0]
        assert get_response.data["item"][1]["id"] == data["item"][1]
        assert get_response.data["item"][2]["id"] == data["item"][2]

    def test_watchlist_patch_update(self):
        """
        Ensure we can update fields for a watchlist by patch method
        """

        data = {
            "item": [
                self.item_1.id,
                self.item_2.id,
                self.item_3.id,
            ],
        }
        response = self.post_watchlist(data)

        url = reverse("watchlist-detail", None, {response.data["id"]})
        new_data = {
            "item": [
                self.item_2.id,
            ]
        }
        patch_response = self.client.patch(url, new_data, format="json")

        assert patch_response.status_code == status.HTTP_200_OK
        assert len(patch_response.data["item"]) == 1
        assert patch_response.data["item"][0] == new_data["item"][0]

    def test_watchlist_put_update(self):
        """
        Ensure we can update fields for a watchlist by put method
        """

        data = {
            "item": [
                self.item_1.id,
                self.item_2.id,
                self.item_3.id,
            ],
        }
        response = self.post_watchlist(data)

        url = reverse("watchlist-detail", None, {response.data["id"]})
        new_data = {
            "item": [
                self.item_1.id,
                self.item_2.id,
            ],
        }
        put_response = self.client.put(url, new_data, format="json")

        assert put_response.status_code == status.HTTP_200_OK
        assert len(put_response.data["item"]) == 2
        assert put_response.data["item"][0] == new_data["item"][0]
        assert put_response.data["item"][1] == new_data["item"][1]


class TestOffer(APITestCase):
    """Test class for Offer model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        self.user_1 = User.objects.create_user(username="test_user1", password="test1")
        self.client.login(username="test_user1", password="test1")

        self.currency = Currency.objects.get_or_create(
            code="USD", defaults={"name": "American dollar"}
        )

        self.item_1 = Item.objects.create(
            code="AAPL", name="Apple", details="Stocks of Apple Inc."
        )
        self.item_2 = Item.objects.create(
            code="AMZN", name="Amazon", details="Stocks of Amazon"
        )

    def post_offer(self, data):
        """Post price instance into database through web-api"""

        url = reverse("offer-list")
        response = self.client.post(url, data, format="json")
        return response

    def test_offer_post(self):
        """
        Ensure we can post offer instance
        """

        data = {
            "item": self.item_1.id,
            "status": "PURCHASE",
            "entry_quantity": 10,
            "price": Decimal("100"),
            "is_active": True,
        }
        response = self.post_offer(data)
        print(response.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Offer.objects.count() == 1
        assert Offer.objects.get().user == self.user_1
        assert Offer.objects.get().item == self.item_1
        assert Offer.objects.get().status == data["status"]
        assert Offer.objects.get().entry_quantity == data["entry_quantity"]
        assert Offer.objects.get().price == data["price"]
        assert Offer.objects.get().is_active == data["is_active"]

    def test_offers_list(self):
        """
        Ensure we can retrieve the offers collection
        """

        data_offer_1 = {
            "item": self.item_1.id,
            "status": "PURCHASE",
            "entry_quantity": 6,
            "price": Decimal("100.00"),
            "is_active": True,
        }
        self.post_offer(data_offer_1)

        data_offer_2 = {
            "item": self.item_2.id,
            "status": "SELL",
            "entry_quantity": 7,
            "price": Decimal("40.00"),
            "is_active": True,
        }
        self.post_offer(data_offer_2)

        url = reverse("offer-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

        assert response.data["results"][0]["user"]["username"] == self.user_1.username
        assert response.data["results"][0]["item"]["id"] == data_offer_1["item"]
        assert response.data["results"][0]["status"] == data_offer_1["status"]
        assert (
            response.data["results"][0]["entry_quantity"]
            == data_offer_1["entry_quantity"]
        )
        assert response.data["results"][0]["quantity"] == 0
        assert response.data["results"][0]["price"] == data_offer_1["price"].__str__()
        assert response.data["results"][0]["is_active"] == data_offer_1["is_active"]

        assert response.data["results"][1]["user"]["username"] == self.user_1.username
        assert response.data["results"][1]["item"]["id"] == data_offer_2["item"]
        assert response.data["results"][1]["status"] == data_offer_2["status"]
        assert (
            response.data["results"][1]["entry_quantity"]
            == data_offer_2["entry_quantity"]
        )
        assert response.data["results"][1]["quantity"] == 0
        assert response.data["results"][1]["price"] == data_offer_2["price"].__str__()
        assert response.data["results"][1]["is_active"] == data_offer_2["is_active"]

    def test_offer_get(self):
        """
        Ensure we can get a single offer by id
        """

        data = {
            "item": self.item_2.id,
            "status": "SELL",
            "entry_quantity": 700,
            "price": Decimal("3222.23"),
            "is_active": True,
        }
        response = self.post_offer(data)

        url = reverse("offer-detail", None, {response.data["id"]})
        get_response = self.client.get(url, format="json")

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data["user"]["username"] == self.user_1.username
        assert get_response.data["item"]["id"] == data["item"]
        assert get_response.data["status"] == data["status"]
        assert get_response.data["entry_quantity"] == data["entry_quantity"]
        assert get_response.data["quantity"] == 0
        assert get_response.data["price"] == data["price"].__str__()
        assert get_response.data["is_active"] == data["is_active"]

    def test_offer_patch_update(self):
        """
        Ensure we can update fields for a offer by patch method
        """

        data = {
            "item": self.item_2.id,
            "status": "SELL",
            "entry_quantity": 700,
            "price": Decimal("3222.23"),
            "is_active": True,
        }
        response = self.post_offer(data)

        url = reverse("offer-detail", None, {response.data["id"]})
        new_data = {
            "item": self.item_1.id,
            "entry_quantity": 701,
            "price": Decimal("3243.23"),
        }
        patch_response = self.client.patch(url, new_data, format="json")

        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data["item"] == new_data["item"]
        assert patch_response.data["status"] == data["status"]
        assert patch_response.data["entry_quantity"] == new_data["entry_quantity"]
        assert patch_response.data["quantity"] == 0
        assert patch_response.data["price"] == new_data["price"].__str__()
        assert patch_response.data["is_active"] == data["is_active"]

    def test_offer_put_update(self):
        """
        Ensure we can update fields for a offer by put method
        """

        data = {
            "item": self.item_2.id,
            "status": "SELL",
            "entry_quantity": 700,
            "price": Decimal("3222.23"),
            "is_active": True,
        }
        response = self.post_offer(data)

        url = reverse("offer-detail", None, {response.data["id"]})
        new_data = {
            "item": self.item_1.id,
            "status": "PURCHASE",
            "entry_quantity": 2131,
            "price": Decimal("32212.23"),
            "is_active": True,
        }
        put_response = self.client.patch(url, new_data, format="json")

        assert put_response.status_code == status.HTTP_200_OK
        assert put_response.data["item"] == new_data["item"]
        assert put_response.data["status"] == new_data["status"]
        assert put_response.data["entry_quantity"] == new_data["entry_quantity"]
        assert put_response.data["quantity"] == 0
        assert put_response.data["price"] == new_data["price"].__str__()
        assert put_response.data["is_active"] == new_data["is_active"]

    def test_offer_delete(self):
        """
        Ensure we can delete a single offer instance
        """

        data = {
            "item": self.item_2.id,
            "status": "SELL",
            "entry_quantity": 700,
            "price": Decimal("3222.23"),
            "is_active": True,
        }
        response = self.post_offer(data)

        url = reverse("offer-detail", None, {response.data["id"]})
        delete_response = self.client.delete(url, format="json")

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        assert Offer.objects.get().is_active == False
        assert response.data["id"] == Offer.objects.get().id


class TestBalance(APITestCase):
    """Test class for Balance model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        self.user_1 = User.objects.create_user(username="test_user", password="test")
        self.user_2 = User.objects.create_user(username="test_user2", password="test")
        self.client.login(username="test_user", password="test")

        self.currency_1 = Currency.objects.create(
            name="American Dollar",
            code="USD",
        )
        self.currency_2 = Currency.objects.create(
            name="Euro",
            code="EUR",
        )

    def test_balance_list(self):
        """
        Ensure we can retrieve the balances collection
        """

        data_balance_1 = {
            "user": self.user_1,
            "currency": self.currency_1,
            "quantity": 200,
        }
        Balance.objects.create(**data_balance_1)

        data_balance_2 = {
            "user": self.user_2,
            "currency": self.currency_2,
            "quantity": 500,
        }
        Balance.objects.create(**data_balance_2)

        url = reverse("balance-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

        assert response.data["results"][0]["user"]["username"] == self.user_1.username
        assert (
            response.data["results"][0]["currency"]["code"]
            == data_balance_1["currency"].code
        )
        assert response.data["results"][0]["quantity"] == data_balance_1["quantity"]

        assert response.data["results"][1]["user"]["username"] == self.user_2.username
        assert (
            response.data["results"][1]["currency"]["code"]
            == data_balance_2["currency"].code
        )
        assert response.data["results"][1]["quantity"] == data_balance_2["quantity"]

    def test_balance_get(self):
        """
        Ensure we can get a single balance by id
        """

        data = {
            "user": self.user_2,
            "currency": self.currency_2,
            "quantity": 500,
        }
        balance = Balance.objects.create(**data)

        url = reverse("balance-detail", None, {balance.id})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["user"]["username"] == self.user_2.username
        assert response.data["currency"]["code"] == data["currency"].code
        assert response.data["quantity"] == data["quantity"]


class TestInventory(APITestCase):
    """Test class for Inventory model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        self.user_1 = User.objects.create_user(username="test_user", password="test")
        self.user_2 = User.objects.create_user(username="test_user2", password="test")
        self.client.login(username="test_user", password="test")

        self.item_1 = Item.objects.create(
            name="Apple",
            code="AAPL",
        )
        self.item_2 = Item.objects.create(
            name="Tesla",
            code="TSLA",
        )

    def test_inventory_list(self):
        """
        Ensure we can retrieve the inventories collection
        """

        data_inventory_1 = {
            "user": self.user_1,
            "item": self.item_1,
            "quantity": 90,
        }
        Inventory.objects.create(**data_inventory_1)

        data_inventory_2 = {
            "user": self.user_2,
            "item": self.item_2,
            "quantity": 200,
        }
        Inventory.objects.create(**data_inventory_2)

        url = reverse("inventory-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

        assert (
            response.data["results"][0]["user"]["username"]
            == data_inventory_1["user"].username
        )
        assert (
            response.data["results"][0]["item"]["code"] == data_inventory_1["item"].code
        )
        assert response.data["results"][0]["quantity"] == data_inventory_1["quantity"]

        assert (
            response.data["results"][1]["user"]["username"]
            == data_inventory_2["user"].username
        )
        assert (
            response.data["results"][1]["item"]["code"] == data_inventory_2["item"].code
        )
        assert response.data["results"][1]["quantity"] == data_inventory_2["quantity"]

    def test_inventory_get(self):
        """
        Ensure we can get a single inventory by id
        """

        data = {
            "user": self.user_1,
            "item": self.item_1,
            "quantity": 90,
        }
        inventory = Inventory.objects.create(**data)

        url = reverse("inventory-detail", None, {inventory.id})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["user"]["username"] == data["user"].username
        assert response.data["item"]["code"] == data["item"].code
        assert response.data["quantity"] == data["quantity"]


class TestTrade(APITestCase):
    """Test class for Trade model"""

    def setUp(self):
        """Initialize necessary fields for testing"""

        self.test_user_1 = User.objects.create_user(
            username="test_user", password="test"
        )
        self.test_user_2 = User.objects.create_user(
            username="test_user2", password="test"
        )

        self.client.login(username="test_user", password="test")

        self.item = Item.objects.create(
            name="Apple",
            code="AAPL",
        )

        self.purchase_offer = Offer.objects.create(
            item=self.item,
            user=self.test_user_1,
            status="PURCHASE",
            entry_quantity=10,
            price=123.12,
            is_active=True,
        )
        self.sell_offer_1 = Offer.objects.create(
            user=self.test_user_1,
            item=self.item,
            status="SELL",
            entry_quantity=10,
            price=123.12,
            is_active=True,
        )
        self.sell_offer_2 = Offer.objects.create(
            user=self.test_user_2,
            item=self.item,
            status="SELL",
            entry_quantity=50,
            price=123.12,
            is_active=True,
        )

    def test_trades_list(self):
        """
        Ensure we can retrieve the trades collection
        """

        data_trade_1 = {
            "item": self.item,
            "seller": self.test_user_1,
            "buyer": self.test_user_2,
            "quantity": 10,
            "unit_price": Decimal("2303.00"),
            "description": "Trade between two users",
            "buyer_offer": self.purchase_offer,
            "seller_offer": self.sell_offer_1,
        }
        Trade.objects.create(**data_trade_1)

        data_trade_2 = {
            "item": self.item,
            "seller": self.test_user_2,
            "buyer": self.test_user_1,
            "quantity": 10,
            "unit_price": Decimal("2500.00"),
            "description": "AAPL trade between two users",
            "buyer_offer": self.purchase_offer,
            "seller_offer": self.sell_offer_2,
        }
        Trade.objects.create(**data_trade_2)

        url = reverse("trade-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

        assert response.data["results"][0]["item"]["id"] == data_trade_1["item"].id
        assert response.data["results"][0]["seller"] == data_trade_1["seller"].username
        assert response.data["results"][0]["buyer"] == data_trade_1["buyer"].username
        assert response.data["results"][0]["quantity"] == data_trade_1["quantity"]
        assert (
            response.data["results"][0]["unit_price"]
            == data_trade_1["unit_price"].__str__()
        )
        assert response.data["results"][0]["description"] == data_trade_1["description"]

        offer_response = self.client.get(response.data["results"][0]["buyer_offer"])
        assert offer_response.data["id"] == data_trade_1["buyer_offer"].id

        offer_response = self.client.get(response.data["results"][0]["seller_offer"])
        assert offer_response.data["id"] == data_trade_1["seller_offer"].id

        assert response.data["results"][1]["item"]["id"] == data_trade_2["item"].id
        assert response.data["results"][1]["seller"] == data_trade_2["seller"].username
        assert response.data["results"][1]["buyer"] == data_trade_2["buyer"].username
        assert response.data["results"][1]["quantity"] == data_trade_2["quantity"]
        assert (
            response.data["results"][1]["unit_price"]
            == data_trade_2["unit_price"].__str__()
        )
        assert response.data["results"][1]["description"] == data_trade_2["description"]

        offer_response = self.client.get(response.data["results"][1]["buyer_offer"])
        assert offer_response.data["id"] == data_trade_2["buyer_offer"].id

        offer_response = self.client.get(response.data["results"][1]["seller_offer"])
        assert offer_response.data["id"] == data_trade_2["seller_offer"].id

    def test_trade_get(self):
        """
        Ensure we can get a single trade by id
        """

        data = {
            "item": self.item,
            "seller": self.test_user_1,
            "buyer": self.test_user_2,
            "quantity": 10,
            "unit_price": Decimal("2303.00"),
            "description": "Trade between two users",
            "buyer_offer": self.purchase_offer,
            "seller_offer": self.sell_offer_1,
        }
        trade = Trade.objects.create(**data)

        url = reverse("trade-detail", None, {trade.id})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["item"]["id"] == data["item"].id
        assert response.data["seller"] == data["seller"].username
        assert response.data["buyer"] == data["buyer"].username
        assert response.data["quantity"] == data["quantity"]
        assert response.data["unit_price"] == data["unit_price"].__str__()
        assert response.data["description"] == data["description"]

        offer_response = self.client.get(response.data["buyer_offer"])
        assert offer_response.data["id"] == data["buyer_offer"].id

        offer_response = self.client.get(response.data["seller_offer"])
        assert offer_response.data["id"] == data["seller_offer"].id
