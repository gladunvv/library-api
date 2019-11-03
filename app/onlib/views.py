from rest_framework.views import APIView
from rest_framework import permissions
from onlib.models import Book
from onlib.serializers import BookSerializer
from rest_framework import filters
from rest_framework import generics

from django_filters import rest_framework as filter_rest


class AllBooksView(generics.ListAPIView):

    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title',]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class FilterBooksView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filter_rest.DjangoFilterBackend,)
    filterset_fields = ('genre', 'author')
