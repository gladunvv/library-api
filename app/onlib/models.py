from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='First name')
    last_name = models.CharField(max_length=255, verbose_name='Last name')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Date of birth')
    date_of_death = models.DateField(blank=True, null=True, verbose_name='Date of death')

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Genre(models.Model):
    title = models.CharField(max_length=255, verbose_name='Book\'s genre')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Book title')
    description = models.TextField(blank=True, verbose_name='Book description')
    page_amount = models.IntegerField(verbose_name='Amount page book')
    isbn = models.CharField(max_length=255, verbose_name='Book ISBN')
    author = models.ForeignKey(Author, related_name='books_author', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, related_name='books_genre', on_delete=models.CASCADE)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title
