# Generated by Django 2.2.6 on 2019-11-02 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlib', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='description',
        ),
    ]
