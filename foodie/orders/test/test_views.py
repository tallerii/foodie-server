from rest_framework.test import APITestCase
from django.urls import reverse

from rest_framework import status

from foodie.orders.test.dummies import getOrderDummy
from foodie.users.test.dummies import getUserDummy

class OrderListTestCase(APITestCase):
    """
    Tests /clients list operations.
    """
    def setUp(self):
        self.user_data = getUserDummy()
        self.client.post(reverse('clients-list'), self.user_data)
        credentials = {'username': self.user_data.get('username'), 'password': self.user_data.get('password')}
        token_response = self.client.post('/token-auth/username', credentials)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_response.data.get("token")}')
        self.url = reverse('orders-list')
        self.order_data = getOrderDummy()

    def test_post(self):
        response = self.client.post(self.url, self.order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_assigns_client_to_authed_user(self):
        self.client.post(self.url, self.order_data)
        order = self.client.get(self.url).data.get('results')[0]
        self.assertEqual(order.get('client_user').get('properties').get('username'), self.user_data.get('username'))

    def test_create_starts_with_status_unassigned(self):
        self.client.post(self.url, self.order_data)
        order = self.client.get(self.url).data.get('results')[0]
        self.assertEqual(order.get('status'), 'unassigned')

    def test_create_starts_with_no_delivery(self):
        self.client.post(self.url, self.order_data)
        order = self.client.get(self.url).data.get('results')[0]
        self.assertEqual(order.get('delivery_user'), None)
