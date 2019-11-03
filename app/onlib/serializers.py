from rest_framework import serializers

from onlib.models import Book, Author, Genre


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'title')


class BookSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()
    genre = GenreSerializer()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'genre')


class FullAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name', 'date_of_birth', 'date_of_death')


class FullBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'page_amount', 'isbn')
