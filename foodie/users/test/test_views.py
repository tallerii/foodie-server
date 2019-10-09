from django.urls import reverse
from django.contrib.auth.hashers import check_password
from rest_framework.test import APITestCase
from rest_framework import status
from foodie.users.models import User
from foodie.users.test.dummies import getUserDummy, getUserDummy2


class TestClientListTestCase(APITestCase):
    """
    Tests /clients list operations.
    """
    def setUp(self):
        self.url = reverse('clients-list')
        self.user_data = getUserDummy()

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_request_with_valid_data_creates_new_user(self):
        response = self.client.post(self.url, self.user_data)
        try:
            User.objects.get(pk=response.data.get('id'))
        except User.DoesNotExist:
            self.fail()
        except User.MultipleObjectsReturned:
            self.fail()

    def test_post_request_with_valid_data_creates_new_client(self):
        response = self.client.post(self.url, self.user_data)
        user = User.objects.get(pk=response.data.get('id'))
        self.assertFalse(user.is_delivery)

    def test_post_request_with_valid_data_creates_new_client_with_specified_data(self):
        response = self.client.post(self.url, self.user_data)
        user = User.objects.get(pk=response.data.get('id'))
        self.assertEqual(user.username, self.user_data.get('username'))
        self.assertTrue(check_password(self.user_data.get('password'), user.password))
        self.assertEqual(user.first_name, self.user_data.get('first_name'))
        self.assertEqual(user.last_name, self.user_data.get('last_name'))
        self.assertEqual(user.email, self.user_data.get('email'))
        self.assertEqual(user.phone_number, self.user_data.get('phone_number'))

    def test_post_request_with_valid_data_creates_new_client_that_is_not_premium(self):
        response = self.client.post(self.url, self.user_data)
        user = User.objects.get(pk=response.data.get('id'))
        self.assertFalse(user.is_premium)

    def test_post_request_with_valid_data_creates_new_client_with_initial_reputation_2_and_a_half(self):
        response = self.client.post(self.url, self.user_data)
        user = User.objects.get(pk=response.data.get('id'))
        self.assertEqual(2.5, user.reputation)

    def test_post_request_with_valid_data_creates_new_client_without_initial_loction(self):
        response = self.client.post(self.url, self.user_data)
        user = User.objects.get(pk=response.data.get('id'))
        self.assertIsNone(user.lat)
        self.assertIsNone(user.lon)


class TestDeliveryListTestCase(APITestCase):
    """
    Tests /deliveries list operations.
    """
    def setUp(self):
        self.url = reverse('deliveries-list')
        self.user_data = getUserDummy()

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_request_with_valid_data_creates_new_user(self):
        response = self.client.post(self.url, self.user_data)
        try:
            User.objects.get(pk=response.data.get('id'))
        except User.DoesNotExist:
            self.fail()
        except User.MultipleObjectsReturned:
            self.fail()

    def test_post_request_with_valid_data_creates_new_delivery(self):
        response = self.client.post(self.url, self.user_data)
        user = User.objects.get(pk=response.data.get('id'))
        self.assertTrue(user.is_delivery)
    
    def test_post_request_with_valid_data_creates_new_delivery_with_specified_data(self):
        response = self.client.post(self.url, self.user_data)
        user = User.objects.get(pk=response.data.get('id'))
        self.assertEqual(user.username, self.user_data.get('username'))
        self.assertTrue(check_password(self.user_data.get('password'), user.password))
        self.assertEqual(user.first_name, self.user_data.get('first_name'))
        self.assertEqual(user.last_name, self.user_data.get('last_name'))
        self.assertEqual(user.email, self.user_data.get('email'))
        self.assertEqual(user.phone_number, self.user_data.get('phone_number'))

    def test_post_request_with_valid_data_creates_new_delivery_that_is_not_premium(self):
        response = self.client.post(self.url, self.user_data)
        user = User.objects.get(pk=response.data.get('id'))
        self.assertFalse(user.is_premium)

    def test_post_request_with_valid_data_creates_new_delivery_with_initial_reputation_2_and_a_half(self):
        response = self.client.post(self.url, self.user_data)
        user = User.objects.get(pk=response.data.get('id'))
        self.assertEqual(2.5, user.reputation)

    def test_post_request_with_valid_data_creates_new_delivery_without_initial_loction(self):
        response = self.client.post(self.url, self.user_data)
        user = User.objects.get(pk=response.data.get('id'))
        self.assertIsNone(user.lat)
        self.assertIsNone(user.lon)


class TestClientDetailTestCase(APITestCase):
    """
    Tests /clients detail operations.
    """
    def setUp(self):
        self.self_data = getUserDummy()
        self.other_data = getUserDummy2()
        create_self_response = self.client.post(reverse('clients-list'), self.self_data)
        create_other_response = self.client.post(reverse('clients-list'), self.other_data)
        self_credentials = {'username': self.self_data.get('username'), 'password': self.self_data.get('password')}
        auth_token_response = self.client.post('/token-auth/username/', self_credentials)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token_response.data.get("token")}')
        self_id = create_self_response.data.get('id')
        other_id = create_other_response.data.get('id')
        self.selfUrl = reverse('clients-detail', kwargs={'pk': self_id})
        self.otherUrl = reverse('clients-detail', kwargs={'pk': other_id})
        self.invalidUrl = reverse('clients-detail', kwargs={'pk': 'invalidpk'})

    def test_get_request_with_invalid_pk_fails(self):
        response = self.client.get(self.invalidUrl)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_request_with_valid_pk_from_same_client_suceeds(self):
        response = self.client.get(self.selfUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_valid_pk_from_other_client_suceeds(self):
        response = self.client.get(self.otherUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_valid_pk_from_same_user_returns_all_data(self):
        response = self.client.get(self.selfUrl)
        self.assertIn('username', response.data)
        self.assertIn('avatar', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone_number', response.data)
        self.assertIn('is_premium', response.data)
        self.assertIn('is_delivery', response.data)
        self.assertIn('reputation', response.data)
        self.assertIn('lat', response.data)
        self.assertIn('lon', response.data)
        self.assertIn('location_last_updated', response.data)

    def test_get_request_with_valid_pk_from_other_user_returns_public_data_only(self):
        response = self.client.get(self.otherUrl)
        self.assertIn('username', response.data)
        self.assertIn('avatar', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertNotIn('email', response.data)
        self.assertNotIn('phone_number', response.data)
        self.assertIn('is_premium', response.data)
        self.assertIn('is_delivery', response.data)
        self.assertIn('reputation', response.data)
        self.assertIn('lat', response.data)
        self.assertIn('lon', response.data)
        self.assertIn('location_last_updated', response.data)

    # def test_put_request_updates_a_user(self):
    #     new_first_name = fake.first_name()
    #     payload = {'first_name': new_first_name}
    #     response = self.client.put(self.url, payload)
    #     eq_(response.status_code, status.HTTP_200_OK)

    #     user = User.objects.get(pk=self.user.id)
    #     eq_(user.first_name, new_first_name)
