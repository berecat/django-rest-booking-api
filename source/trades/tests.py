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
        """Initialize necessary fields for testing"""

        User.objects.create_user(username='test_user',
                                 password='test')
        self.client.login(username='test_user',
                          password='test')

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