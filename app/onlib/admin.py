from django.contrib import admin
from onlib.models import Author, Book, Genre


@admin.register(Book)
class AdminBook(admin.ModelAdmin):

    list_display = ('title',)


@admin.register(Genre)
class AdminGenre(admin.ModelAdmin):

    list_display = ('title',)


@admin.register(Author)
class AdminAuthor(admin.ModelAdmin):

    list_display = ('first_name', 'last_name')

