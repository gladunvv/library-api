from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from onlib.models import Book, Author, Genre
from onlib.serializers import BookSerializer
from rest_framework import filters
from rest_framework import generics


class AllBooksView(generics.ListAPIView):

    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title',]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
