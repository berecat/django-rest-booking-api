from django.urls import reverse
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
    def test_list_check_status(self):
        url = reverse('currency-list')
        response = self.client.get(url)
        assert response.status_code == 200
