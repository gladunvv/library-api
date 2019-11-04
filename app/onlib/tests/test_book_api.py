from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from rest_framework import status

from onlib.models import Book, Genre, Author


CREATE_USER_URL = reverse('users:create_user')
SEARCH_BOOK_URL = reverse('onlib:search')
BOOK_URL = reverse('onlib:books')


def sample_book_onlib():

    data_genre = {
        'title': 'Someone title',
    }
    Genre.objects.create(**data_genre)

    data_author = {
        'first_name': 'Someone',
        'last_name': 'Author',
    }
    Author.objects.create(**data_author)

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

    def test_search_book_no_auth(self):
        sample_book_onlib()
        res = self.client.get(SEARCH_BOOK_URL + '?search=Siddhartha')
        self.assertEqual(res.data[0]['title'], 'Siddhartha')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_search_book_auth(self):
        sample_book_onlib()
        jwt_token = self.user_jwt()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.get(SEARCH_BOOK_URL + '?search=Spoke')
        self.assertEqual(res.data[0]['title'], 'Thus Spoke Zarathustra')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_book_models_str_method(self):
        data = {
                'title': 'Flowers for Algernon',
                'description': 'Long description',
                'page_amount': 342,
                'isbn': '9788467511468',
                'genre_id': 1,
                'author_id': 1,
                }
        Genre.objects.create(
            title='Test Genre')
        Author.objects.create(
            first_name='Test',
            last_name='Author')
        item = Book.objects.create(**data)
        self.assertEqual(str(item), 'Flowers for Algernon')

    def test_books_get_not_auth(self):
        sample_book_onlib()
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_books_get_authorizerd(self):
        sample_book_onlib()
        jwt_token = self.user_jwt()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_books_post_not_staff(self):
        context = {
            'title': 'Flowers for Algernon',
            'description': 'Long description',
            'page_amount': 342,
            'isbn': '9788467511468',
            'genre_id': 1,
            'author_id': 1,
        }
        sample_book_onlib()
        jwt_token = self.user_jwt()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.post(BOOK_URL, context)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_books_post_staff(self):
        context = {
            'title': 'Flowers for Algernon',
            'description': 'Long description',
            'page_amount': 342,
            'isbn': '9788467511468',
            'genre_id': 1,
            'author_id': 1,
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.post(BOOK_URL, context)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_books_post_staff_bad_data(self):
        context = {
            'title': 'Flowers for Algernon',
            'descripton': 'Long description',
            'page_amunt': 342,
            'isb': '9788467511468',
            'genre_id': 1,
            'author_id': 1,
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.post(BOOK_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_put(self):
        context = {
            'title': 'Flowers for Algernon',
            'description': 'Long description',
            'page_amount': 342,
            'isbn': '9788467511468',
            'genre_id': 1,
            'author_id': 1,
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.put(BOOK_URL + '?book=1', context)
        book = Book.objects.get(pk=1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(context['title'], book.title)

    def test_book_put_not_book_in_url(self):
        context = {
            'title': 'Flowers for Algernon',
            'description': 'Long description',
            'page_amount': 342,
            'isbn': '9788467511468',
            'genre_id': 1,
            'author_id': 1,
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.put(BOOK_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['errors'], 'No book provided')

    def test_book_put_in_url_no_int(self):
        context = {
            'title': 'Flowers for Algernon',
            'description': 'Long description',
            'page_amount': 342,
            'isbn': '9788467511468',
            'genre_id': 1,
            'author_id': 1,
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.put(BOOK_URL + '?book=abd', context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['errors'], 'Argument must be int')

    def test_book_put_bad_data(self):
        context = {
            'title': 'Flowers for Algernon',
            'deription': 'Long description',
            'pa_amount': 342,
            'isb': '9788467511468',
            'genre_id': 1,
            'author_id': 1,
        }
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.put(BOOK_URL + '?book=1', context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_delete(self):
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.delete(BOOK_URL + '?book=1')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_book_delete_not_book(self):
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.delete(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['errors'], 'No book provided')

    def test_book_delete_in_url_no_int(self):
        sample_book_onlib()
        jwt_token = self.user_jwt(is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        res = self.client.delete(BOOK_URL + '?book=abd')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['errors'], 'Argument must be int')
