from django.urls import path

from onlib.views import (
    SearchBooksView,
    FilterBooksView,
    AuthorView,
    GenreView,
    BookView
)

app_name = 'onlib'

urlpatterns = [
    path('search', SearchBooksView.as_view(), name='search'),
    path('filter', FilterBooksView.as_view(), name='filter'),
    path('genres', GenreView.as_view(), name='genres'),
    path('authors', AuthorView.as_view(), name='authors'),
    path('book', BookView.as_view(), name='books'),
]
