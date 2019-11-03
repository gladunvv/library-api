from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from onlib.models import Book, Genre, Author


SEARCH_BOOK_URL = reverse('onlib:search')


CREATE_USER_URL = reverse('users:create_user')


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

    def test_search_book_no_auth(self):
        sample_book_onlib()
        res = self.client.get(SEARCH_BOOK_URL + '?search=Siddhartha')
        self.assertEqual(res.data[0]['title'], 'Siddhartha')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_search_book_auth(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }
        sample_book_onlib()
        res_user = self.client.post(CREATE_USER_URL, context)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res_user.data['access'])
        res = self.client.get(SEARCH_BOOK_URL + '?search=Spoke')
        self.assertEqual(res.data[0]['title'], 'Thus Spoke Zarathustra')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_author_models_str_method(self):
        item = Author.objects.create(
            first_name='Test',
            last_name='Author'
            )
        self.assertEqual(str(item), 'Test Author')

    def test_genre_models_str_method(self):
        item = Genre.objects.create(
            title='Test Genre'
            )
        self.assertEqual(str(item), 'Test Genre')

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
