from django.urls import path
from onlib.views import AllBooksView, FilterBooksView

app_name = 'onlib'

urlpatterns = [
    path('search', AllBooksView.as_view(), name='search'),
    path('filter', FilterBooksView.as_view(), name='filter'),
]