from rest_framework import permissions
from rest_framework import generics
from rest_framework import filters

from django_filters import rest_framework as filter_rest

from onlib.models import Book
from onlib.serializers import BookSerializer


class AllBooksView(generics.ListAPIView):

    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class FilterBooksView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filter_rest.DjangoFilterBackend,)
    filterset_fields = ('genre', 'author')
    queryset = Book.objects.all()
    serializer_class = BookSerializer
