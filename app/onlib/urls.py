from django.urls import path
from onlib.views import AllBooksView, FilterBooksView

app_name = 'onlib'

urlpatterns = [
    path('books', AllBooksView.as_view(), name='all_book'),
    path('filter', FilterBooksView.as_view(), name='filter'),
]