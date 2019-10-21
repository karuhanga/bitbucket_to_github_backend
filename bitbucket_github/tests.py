from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch

from bitbucket_github.views import LoginSerializer, User
from bitbucket_github.serializers import requests


class ViewTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.test_username = "test_user_logout"
        cls.user = User(username=cls.test_username, github_token=12, bitbucket_token=34)
        cls.user.set_unusable_password()
        cls.user.save()

    def test_login(self):
        test_username = "test_user_login"
        self.assertRaises(User.DoesNotExist, User.objects.get, username=test_username)

        with patch.object(LoginSerializer, 'validate_bitbucket_token', return_value='random_token'):
            with patch.object(User, 'github_authenticated', return_value=True):
                response = self.api_client.post(reverse('login'),
                                                {'username': test_username, 'bitbucket_token': 'random_token'}, format='json')

                self.assertEqual(response.status_code, HTTP_200_OK)
                self.assertEqual(response.data['username'], test_username)
                self.assertEqual(response.data['githubAuthenticated'], True)
                self.assertIsInstance(User.objects.get(username=test_username), User)

    def test_logout(self):
        self.api_client.force_authenticate(self.user)

        response = self.api_client.post(reverse('logout'))
        self.assertEqual(response.status_code, HTTP_200_OK)

        updated_user = User.objects.get(username=self.test_username)
        self.assertEqual(updated_user.bitbucket_token, None)
        self.assertEqual(updated_user.github_token, None)

    def test_authorize_github_success(self):
        class MockPostRequest:
            status_code = HTTP_200_OK

            @staticmethod
            def json():
                return {'access_token': '12'}

        self.api_client.force_authenticate(self.user)

        with patch.object(requests, 'post', return_value=MockPostRequest()):
            response = self.api_client.post(reverse('authorize_github'), {'code': 12}, format='json')

            self.assertEqual(response.status_code, HTTP_200_OK)
            self.assertEqual(response.data, {
                'message': "Successfully authorized github",
            })

    def test_authorize_github_fail(self):
        class MockPostRequest:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR

        self.api_client.force_authenticate(self.user)

        with patch.object(requests, 'post', return_value=MockPostRequest()):
            response = self.api_client.post(reverse('authorize_github'), {'code': 12}, format='json')

            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['code'][0], 'Github code is invalid')
