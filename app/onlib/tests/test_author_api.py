from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from rest_framework import status

from onlib.models import Book, Genre, Author


CREATE_USER_URL = reverse('users:create_user')
FILTER_BOOK_URL = reverse('onlib:filter')
AUTHOR_URL = reverse('onlib:authors')


def sample_book_onlib():

    data_genre = {
        'title': 'Someone title',
    }

    Genre.objects.create(**data_genre)

    data_author = [
        {
            'first_name': 'First',
            'last_name': 'Author',
        },
        {
            'first_name': 'Second',
            'last_name': 'Author',
        }
    ]
    for data in data_author:
        Author.objects.create(**data)

    data_books = [
        {
            'title': 'Moral letters to Lucilius',
            'description': 'Long description',
            'page_amount': 242,
            'isbn': '9780486811246',
            'genre_id': 1,
            'author_id': 1,
        },
        {
            'title': 'Siddhartha',
            'description': 'Long description',
            'page_amount': 152,
            'isbn': '9781548460075',
            'genre_id': 1,
            'author_id': 1,
        },
        {
            'title': 'Thus Spoke Zarathustra',
            'description': 'Long description',
            'page_amount': 352,
            'isbn': '9781975638634',
            'genre_id': 1,
            'author_id': 1,
        },
    ]

    for data in data_books:
        Book.objects.create(**data)


class UserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def user_jwt(self, is_staff=False):
        if is_staff:
            user = get_user_model().objects.create(
                username='newuser',
                email='test@bounty.com',
                password='newpass1234',
                is_staff=True,
            )
        else:
            user = get_user_model().objects.create(
                username='newuser',
                email='test@bounty.com',
                password='newpass1234',
            )
        token = RefreshToken.for_user(user)
        return str(token.access_token)

    def test_author_models_str_method(self):
        item = Author.objects.create(
            first_name='Test',
            last_name='Author'
        )
        self.assertEqual(str(item), 'Test Author')

    def test_filter_author_no_auth(self):
        sample_book_onlib()
        res = self.client.get(FILTER_BOOK_URL + '?author=1')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_author_authorized(self):
        sample_book_onlib()
        jwt_token = self.user_jwt()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.get(FILTER_BOOK_URL + '?author=1')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_author_get_not_auth(self):
        sample_book_onlib()
        res = self.client.get(AUTHOR_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_get_authorizerd(self):
        sample_book_onlib()
        jwt_token = self.user_jwt()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.get(AUTHOR_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_author_post_not_staff(self):
        context = {
            'first_name': 'Test',
            'last_name': 'Name',
        }
        sample_book_onlib()
        jwt_token = self.user_jwt()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.post(AUTHOR_URL, context)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_post_staff(self):
        context = {
            'first_name': 'Test',
            'last_name': 'Name',
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.post(AUTHOR_URL, context)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_author_post_staff_bad_data(self):
        context = {
            'firs_name': 'Test',
            'last_nam': 'Name',
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.post(AUTHOR_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_author_put(self):
        context = {
            'first_name': 'Test',
            'last_name': 'Name',
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.put(AUTHOR_URL + '?author=1', context)
        author = Author.objects.get(pk=1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(context['first_name'], author.first_name)

    def test_author_put_not_author_in_url(self):
        context = {
            'first_name': 'Test',
            'last_name': 'Name',
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.put(AUTHOR_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['errors'], 'No author provided')

    def test_author_put_in_url_no_int(self):
        context = {
            'first_name': 'Test',
            'last_name': 'Name',
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.put(AUTHOR_URL + '?author=abd', context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['errors'], 'Argument must be int')

    def test_author_put_bad_data(self):
        context = {
            'firs_name': 'Test',
            'last_name': 'Name',
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.put(AUTHOR_URL + '?author=1', context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_author_delete_with_book(self):
        sample_book_onlib()
        data = Author.objects.get(pk=1)
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.delete(AUTHOR_URL + '?author=1')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'], 'The {last_name} author has books'.format(
            last_name=data.last_name
        ))

    def test_author_delete_not_book(self):
        context = {
            'first_name': 'Test',
            'last_name': 'Name',
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res_author = self.client.post(AUTHOR_URL, context)
        pk = str(res_author.data['id'])
        res = self.client.delete(AUTHOR_URL + '?author=' + pk)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_author_delete_not_author_in_url(self):
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.delete(AUTHOR_URL)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['errors'], 'No author provided')

    def test_author_delete_in_url_no_int(self):
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.delete(AUTHOR_URL + '?author=abd')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['errors'], 'Argument must be int')
