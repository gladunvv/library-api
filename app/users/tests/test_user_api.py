from django.test import TestCase
from django.urls import reverse
from django.core import exceptions
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('users:create_user')
TOKEN_REFRESH_URL = reverse('users:token_refresh')
LOGIN_USER_URL = reverse('users:login')
DELETE_USER_URL = reverse('users:delete')


def create_user(*args, **kwargs):
    return get_user_model().objects.create_user(**kwargs)


class UserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }

        res = self.client.post(CREATE_USER_URL, context)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_user_exists_bad_password(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass',
        }

        res = self.client.post(CREATE_USER_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_exists_bad_email(self):
        context = {
            'username': 'newuser',
            'email': 'testbad',
            'password': 'newpass1234',
        }
        res = self.client.post(CREATE_USER_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }
        create_user(**context)
        res = self.client.post(LOGIN_USER_URL, context)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_user(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }
        res = self.client.post(CREATE_USER_URL, context)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_refresh_token(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }
        res_user = self.client.post(CREATE_USER_URL, context)
        data = {'refresh': res_user.data['refresh']}
        res_token = self.client.post(TOKEN_REFRESH_URL, data)
        self.assertIn('access', res_token.data)
        self.assertEqual(res_token.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }
        res_create = self.client.post(CREATE_USER_URL, context)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + res_create.data['access'])
        res = self.client.delete(DELETE_USER_URL)
        try:
            get_user_model().objects.get(username=res_create.data['username'])
        except exceptions.ObjectDoesNotExist:
            self.assertTrue(True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
