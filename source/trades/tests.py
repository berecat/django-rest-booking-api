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

    def test_currency_update(self):
        """
        Ensure we can update fields for a currency
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