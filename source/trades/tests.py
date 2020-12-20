from decimal import Decimal

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from trades.models import (Currency,
                           Item,
                           Price,
                           WatchList,
                           Offer,
                           Inventory,
                           Trade)
from trades import views


class TestCurrency(APITestCase):
    """Test class for Currency model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        User.objects.create_user(username='test_user',
                                 password='test'
                                 )
        self.client.login(username='test_user',
                          password='test'
                          )

    def post_currency(self, data):
        """Post currency instance into database through web-api"""

        url = reverse('currency-list')
        response = self.client.post(url, data, format='json')
        return response

    def test_currency_post(self):
        """
        Ensure we can post currency instance
        """

        data = {
            'code': 'USD',
            'name': 'American Dollar'
        }
        response = self.post_currency(data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Currency.objects.count() == 1
        assert Currency.objects.get().name == data['name']
        assert Currency.objects.get().code == data['code']

    def test_currencies_list(self):
        """
        Ensure we can retrieve the currencies collection
        """

        data_currency_1 = {
            'code': 'USD',
            'name': 'American Dollar',
        }
        self.post_currency(data_currency_1)

        data_currency_2 = {
            'code': 'EUR',
            'name': 'Euro',
        }
        self.post_currency(data_currency_2)

        url = reverse('currency-list')
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['name'] == data_currency_1['name']
        assert response.data[0]['code'] == data_currency_1['code']
        assert response.data[1]['name'] == data_currency_2['name']
        assert response.data[1]['code'] == data_currency_2['code']

    def test_currency_get(self):
        """
        Ensure we can get a single currency by id
        """

        data = {
            'code': 'USD',
            'name': 'American Dollar'
        }
        response = self.post_currency(data)

        url = reverse('currency-detail', None, {response.data['id']})
        get_response = self.client.get(url, format='json')

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['name'] == data['name']
        assert get_response.data['code'] == data['code']

    def test_currency_patch_update(self):
        """
        Ensure we can update fields for a currency by patch method
        """

        data = {
            'code': 'BYN',
            'name': 'American Dollar'
        }
        response = self.post_currency(data)

        url = reverse('currency-detail', None, {response.data['id']})
        new_data = {
            'code': 'USD',
        }
        patch_response = self.client.patch(url, new_data, format='json')

        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['name'] == data['name']
        assert patch_response.data['code'] == new_data['code']

    def test_currency_put_update(self):
        """
        Ensure we can update fields for a currency by put method
        """

        data = {
            'code': 'USD',
            'name': 'American Dollar'
        }
        response = self.post_currency(data)

        url = reverse('currency-detail', None, {response.data['id']})
        new_data = {
            'code': 'EUR',
            'name': 'EURO',
        }
        put_response = self.client.put(url, new_data, format='json')

        assert put_response.status_code == status.HTTP_200_OK
        assert put_response.data['name'] == new_data['name']
        assert put_response.data['code'] == new_data['code']


class TestItem(APITestCase):
    """Test class for Item model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        User.objects.create_user(username='test_user',
                                 password='test'
                                 )
        self.client.login(username='test_user',
                          password='test'
                          )

    def post_item(self, data):
        """Post item instance into database through web-api"""

        url = reverse('item-list')
        response = self.client.post(url, data, format='json')
        return response

    def test_item_post(self):
        """
        Ensure we can post item instance
        """

        data = {
            'code': 'AAPL',
            'name': 'Apple',
            'details': 'Stocks of Apple Inc.'
        }
        response = self.post_item(data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Item.objects.count() == 1
        assert Item.objects.get().name == data['name']
        assert Item.objects.get().code == data['code']
        assert Item.objects.get().details == data['details']

    def test_items_list(self):
        """
        Ensure we can retrieve the items collection
        """

        data_item_1 = {
            'code': 'AAPL',
            'name': 'Apple',
            'details': 'Stocks of Apple Inc.',
        }
        self.post_item(data_item_1)

        data_item_2 = {
            'code': 'TSLA',
            'name': 'Tesla',
            'details': 'Stocks of Tesla Inc.',
        }
        self.post_item(data_item_2)

        url = reverse('item-list')
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['name'] == data_item_1['name']
        assert response.data[0]['code'] == data_item_1['code']
        assert response.data[0]['details'] == data_item_1['details']
        assert response.data[1]['name'] == data_item_2['name']
        assert response.data[1]['code'] == data_item_2['code']
        assert response.data[1]['details'] == data_item_2['details']

    def test_item_get(self):
        """
        Ensure we can get a single item by id
        """

        data = {
            'code': 'TSLA',
            'name': 'Tesla',
            'details': 'Stocks of Tesla Inc.',
        }
        response = self.post_item(data)

        url = reverse('item-detail', None, {response.data['id']})
        get_response = self.client.get(url, format='json')

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['name'] == data['name']
        assert get_response.data['code'] == data['code']
        assert get_response.data['details'] == data['details']

    def test_item_patch_update(self):
        """
        Ensure we can update fields for a item by patch method
        """

        data = {
            'code': 'TSLA',
            'name': 'Tesla',
            'details': 'Stocks of Tesla Inc.',
        }
        response = self.post_item(data)

        url = reverse('item-detail', None, {response.data['id']})
        new_data = {
            'code': 'AAPL',
            'details': 'Stocks of Apple Inc.',
        }
        patch_response = self.client.patch(url, new_data, format='json')

        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['name'] == data['name']
        assert patch_response.data['code'] == new_data['code']
        assert patch_response.data['details'] == new_data['details']

    def test_item_put_update(self):
        """
        Ensure we can update fields for a item by put method
        """

        data = {
            'code': 'TSLA',
            'name': 'Tesla',
            'details': 'Stocks of Tesla Inc.',
        }
        response = self.post_item(data)

        url = reverse('item-detail', None, {response.data['id']})
        new_data = {
            'code': 'AAPL',
            'name': 'Apple',
            'details': 'Stocks of Apple Inc.',
        }
        put_response = self.client.put(url, new_data, format='json')

        assert put_response.status_code == status.HTTP_200_OK
        assert put_response.data['name'] == new_data['name']
        assert put_response.data['code'] == new_data['code']
        assert put_response.data['details'] == new_data['details']

    def test_item_delete(self):
        """
        Ensure we can delete a single item instance
        """

        data = {
            'code': 'TSLA',
            'name': 'Tesla',
            'details': 'Stocks of Tesla Inc.',
        }
        response = self.post_item(data)

        url = reverse('item-detail', None, {response.data['id']})
        delete_response = self.client.delete(url, format='json')

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        assert Item.objects.count() == 0


class TestWatchlist(APITestCase):
    """Test class for Watchlist model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        self.user_1 = User.objects.create_user(username='test_user',
                                               password='test'
                                               )
        self.user_2 = User.objects.create_user(username='test_user2',
                                               password='test'
                                               )
        self.client.login(username='test_user',
                          password='test'
                          )

        self.item_1 = Item.objects.create(name='Apple',
                                          code='AAPL',
                                          )
        self.item_2 = Item.objects.create(name='Tesla',
                                          code='TSLA',
                                          )
        self.item_3 = Item.objects.create(name='Amazon',
                                          code='AMZN',
                                          )

    def post_watchlist(self, data):
        """Post watchlist instance into database through web-api"""

        url = reverse('watchlist-list')
        response = self.client.post(url, data, format='json')
        return response

    def test_watchlist_post(self):
        """
        Ensure we can post watchlist instance
        """

        data = {
            'user': self.user_1.id,
            'item_id': [self.item_1.id,
                        self.item_2.id
                        ]
        }
        response = self.post_watchlist(data)

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
            'user': self.user_1.id,
            'item_id': [self.item_1.id,
                        self.item_2.id,
                        ]
        }
        self.post_watchlist(data_watchlist_1)

        data_watchlist_2 = {
            'user': self.user_2.id,
            'item_id': [self.item_1.id,
                        self.item_3.id,
                        ]
        }
        self.post_watchlist(data_watchlist_2)

        url = reverse('watchlist-list')
        response = self.client.get(url, format='json')

        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        assert response.data[0]['user'] == data_watchlist_1['user']
        assert len(response.data[0]['item']) == 2
        assert response.data[0]['item'][0]['code'] == self.item_1.code
        assert response.data[0]['item'][1]['code'] == self.item_2.code

        assert response.data[1]['user'] == data_watchlist_2['user']
        assert len(response.data[1]['item']) == 2
        assert response.data[1]['item'][0]['code'] == self.item_1.code
        assert response.data[1]['item'][1]['code'] == self.item_3.code

    def test_watchlist_get(self):
        """
        Ensure we can get a single watchlist by id
        """

        data = {
            'user': self.user_2.id,
            'item_id': [self.item_1.id,
                        self.item_2.id,
                        self.item_3.id,
                        ]
        }
        response = self.post_watchlist(data)

        url = reverse('watchlist-detail', None, {response.data['id']})
        get_response = self.client.get(url, format='json')
        print(get_response.data)

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['user'] == data['user']
        assert len(get_response.data['item']) == 3
        assert get_response.data['item'][0]['code'] == self.item_1.code
        assert get_response.data['item'][1]['code'] == self.item_2.code
        assert get_response.data['item'][2]['code'] == self.item_3.code

    def test_watchlist_patch_update(self):
        """
        Ensure we can update fields for a watchlist by patch method
        """

        data = {
            'user': self.user_2.id,
            'item_id': [self.item_1.id,
                        self.item_2.id,
                        self.item_3.id,
                        ]
        }
        response = self.post_watchlist(data)

        url = reverse('watchlist-detail', None, {response.data['id']})
        new_data = {
            'item_id': [self.item_2.id,]
        }
        patch_response = self.client.patch(url, new_data, format='json')

        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['user'] == data['user']
        assert len(patch_response.data['item']) == 1
        assert patch_response.data['item'][0]['code'] == self.item_2.code

    def test_watchlist_put_update(self):
        """
        Ensure we can update fields for a watchlist by put method
        """

        data = {
            'user': self.user_2.id,
            'item_id': [self.item_1.id,
                        self.item_2.id,
                        self.item_3.id,
                        ]
        }
        response = self.post_watchlist(data)

        url = reverse('watchlist-detail', None, {response.data['id']})
        new_data = {
            'user': self.user_1.id,
            'item_id': [self.item_1.id,
                        self.item_2.id,
                        ]
        }
        put_response = self.client.put(url, new_data, format='json')

        assert put_response.status_code == status.HTTP_200_OK
        assert put_response.data['user'] == new_data['user']
        assert len(put_response.data['item']) == 2
        assert put_response.data['item'][0]['code'] == self.item_1.code
        assert put_response.data['item'][1]['code'] == self.item_2.code


class TestInventory(APITestCase):
    """Test class for Inventory model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        self.user_1 = User.objects.create_user(username='test_user',
                                               password='test'
                                               )
        self.user_2 = User.objects.create_user(username='test_user2',
                                               password='test'
                                               )
        self.client.login(username='test_user',
                          password='test'
                          )

        self.item_1 = Item.objects.create(name='Apple',
                                          code='AAPL',
                                          )
        self.item_2 = Item.objects.create(name='Tesla',
                                          code='TSLA',
                                          )

    def test_inventory_list(self):
        """
        Ensure we can retrieve the inventories collection
        """

        data_inventory_1 = {
            'user': self.user_1,
            'item': self.item_1,
            'quantity': 90,
        }
        Inventory.objects.create(**data_inventory_1)

        data_inventory_2 = {
            'user': self.user_2,
            'item': self.item_2,
            'quantity': 200,
        }
        Inventory.objects.create(**data_inventory_2)

        url = reverse('inventory-list')
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        assert response.data[0]['user'] == data_inventory_1['user'].username
        assert response.data[0]['item'] == data_inventory_1['item'].code
        assert response.data[0]['quantity'] == data_inventory_1['quantity']

        assert response.data[1]['user'] == data_inventory_2['user'].username
        assert response.data[1]['item'] == data_inventory_2['item'].code
        assert response.data[1]['quantity'] == data_inventory_2['quantity']

    def test_inventory_get(self):
        """
        Ensure we can get a single inventory by id
        """

        data = {
            'user': self.user_1,
            'item': self.item_1,
            'quantity': 90,
        }
        inventory = Inventory.objects.create(**data)

        url = reverse('inventory-detail', None, {inventory.id})
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK

        assert response.data['user'] == data['user'].username
        assert response.data['item'] == data['item'].code
        assert response.data['quantity'] == data['quantity']


class TestTrade(APITestCase):
    """Test class for Trade model"""

    def setUp(self):
        """Initialize necessary fields for testing"""

        self.test_user_1 = User.objects.create_user(username='test_user',
                                                    password='test'
                                                    )
        self.test_user_2 = User.objects.create_user(username='test_user2',
                                                    password='test'
                                                    )

        self.client.login(username='test_user',
                          password='test'
                          )

        self.item = Item.objects.create(name='Apple',
                                        code='AAPL',
                                        )

        self.purchase_offer = Offer.objects.create(item=self.item,
                                                   user=self.test_user_1,
                                                   status='PURCHASE',
                                                   entry_quantity=10,
                                                   quantity=15,
                                                   price=123.12,
                                                   is_active=True,
                                                   )
        self.sell_offer_1 = Offer.objects.create(item=self.item,
                                                 user=self.test_user_2,
                                                 status='SELL',
                                                 entry_quantity=10,
                                                 quantity=40,
                                                 price=123.12,
                                                 is_active=True,
                                                 )
        self.sell_offer_2 = Offer.objects.create(item=self.item,
                                                 user=self.test_user_2,
                                                 status='SELL',
                                                 entry_quantity=50,
                                                 quantity=40,
                                                 price=123.12,
                                                 is_active=True,
                                                 )

    def test_trades_list(self):
        """
        Ensure we can retrieve the trades collection
        """

        data_trade_1 = {
            'item': self.item,
            'seller': self.test_user_1,
            'buyer': self.test_user_2,
            'quantity': 10,
            'unit_price': Decimal('2303.00'),
            'description': 'Trade between two users',
            'buyer_offer': self.purchase_offer,
            'seller_offer': self.sell_offer_1,
        }
        Trade.objects.create(**data_trade_1)

        data_trade_2 = {
            'item': self.item,
            'seller': self.test_user_2,
            'buyer': self.test_user_1,
            'quantity': 10,
            'unit_price': Decimal('2500.00'),
            'description': 'AAPL trade between two users',
            'buyer_offer': self.purchase_offer,
            'seller_offer': self.sell_offer_2,
        }
        Trade.objects.create(**data_trade_2)

        url = reverse('trade-list')
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        assert response.data[0]['item']['id'] == data_trade_1['item'].id
        assert response.data[0]['seller'] == data_trade_1['seller'].username
        assert response.data[0]['buyer'] == data_trade_1['buyer'].username
        assert response.data[0]['quantity'] == data_trade_1['quantity']
        assert response.data[0]['unit_price'] == data_trade_1['unit_price'].__str__()
        assert response.data[0]['description'] == data_trade_1['description']

        offer_response = self.client.get(response.data[0]['buyer_offer'])
        assert offer_response.data['id'] == data_trade_1['buyer_offer'].id

        offer_response = self.client.get(response.data[0]['seller_offer'])
        assert offer_response.data['id'] == data_trade_1['seller_offer'].id

        assert response.data[1]['item']['id'] == data_trade_2['item'].id
        assert response.data[1]['seller'] == data_trade_2['seller'].username
        assert response.data[1]['buyer'] == data_trade_2['buyer'].username
        assert response.data[1]['quantity'] == data_trade_2['quantity']
        assert response.data[1]['unit_price'] == data_trade_2['unit_price'].__str__()
        assert response.data[1]['description'] == data_trade_2['description']

        offer_response = self.client.get(response.data[1]['buyer_offer'])
        assert offer_response.data['id'] == data_trade_2['buyer_offer'].id

        offer_response = self.client.get(response.data[1]['seller_offer'])
        assert offer_response.data['id'] == data_trade_2['seller_offer'].id

    def test_trade_get(self):
        """
        Ensure we can get a single trade by id
        """

        data = {
            'item': self.item,
            'seller': self.test_user_1,
            'buyer': self.test_user_2,
            'quantity': 10,
            'unit_price': Decimal('2303.00'),
            'description': 'Trade between two users',
            'buyer_offer': self.purchase_offer,
            'seller_offer': self.sell_offer_1,
        }
        trade = Trade.objects.create(**data)

        url = reverse('trade-detail', None, {trade.id})
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK

        assert response.data['item']['id'] == data['item'].id
        assert response.data['seller'] == data['seller'].username
        assert response.data['buyer'] == data['buyer'].username
        assert response.data['quantity'] == data['quantity']
        assert response.data['unit_price'] == data['unit_price'].__str__()
        assert response.data['description'] == data['description']

        offer_response = self.client.get(response.data['buyer_offer'])
        assert offer_response.data['id'] == data['buyer_offer'].id

        offer_response = self.client.get(response.data['seller_offer'])
        assert offer_response.data['id'] == data['seller_offer'].id