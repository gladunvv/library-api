from django.db import models
from django.contrib.auth import get_user_model


class Author(models.Model):
    first_name = models.CharField(max_length=255, blank=True, verbose_name='First name')
    last_name = models.CharField(max_length=255, blank=True, verbose_name='Last name')
    date_of_birth = models.DateField(blank=True, verbose_name='Date of birth')
    date_of_death = models.DateField(blank=True, verbose_name='Date of death')



class Genre(models.Model):
    title = models.CharField(max_length=255, verbose_name='Genre book')
    description = models.TextField(blank=True, verbose_name='Genre description')


class Book(models.Model):
    pass
