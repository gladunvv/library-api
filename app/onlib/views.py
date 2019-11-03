from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import generics
from rest_framework import filters
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework as filter_rest

from onlib.models import Book, Genre, Author
from onlib.serializers import (
    BookSerializer,
    GenreSerializer,
    FullAuthorSerializer,
    FullBookSerializer,
    )

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

UNSAFE_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']


class CustomPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS and
            request.user and
                request.user.is_authenticated):
            return True
        elif (request.method in UNSAFE_METHODS and
            request.user and
                request.user.is_staff):
            return True
        return False


class SearchBooksView(generics.ListAPIView):

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


class GenreView(APIView):

    permission_classes = (CustomPermissions,)

    def get(self, request, *args, **kwargs):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = GenreSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        genre = request.GET.get('genre', None)
        if not genre:
            return Response({'errors': 'No genre provided'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        item = get_object_or_404(Genre, pk=genre)
        serializer = GenreSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorView(APIView):

    permission_classes = (CustomPermissions,)

    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()
        serializer = FullAuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = FullAuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        author = request.GET.get('author', None)
        if not author:
            return Response({'errors': 'No author provided'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        item = get_object_or_404(Author, pk=author)
        serializer = FullAuthorSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookView(APIView):

    permissions = (CustomPermissions,)

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = FullBookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        author = data['author_id']
        genre = data['genre_id']
        serializer = FullBookSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author_id=author,genre_id=genre)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        book = request.GET.get('book', None)
        if not book:
            return Response({'errors': 'No book provided'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        author = data['author_id']
        genre = data['genre_id']
        item = get_object_or_404(Book, pk=book)
        serializer = FullBookSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save(author_id=author, genre_id=genre)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
