# Generated by Django 2.2.6 on 2019-11-04 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlib', '0005_auto_20191104_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Last name'),
        ),
    ]
