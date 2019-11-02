from django.urls import path
from onlib.views import AllBooksView

app_name = 'onlib'

urlpatterns = [
    path('books', AllBooksView.as_view(), name='all_book')
]