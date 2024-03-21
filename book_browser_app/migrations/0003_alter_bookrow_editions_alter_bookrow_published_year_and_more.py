# Generated by Django 4.2 on 2024-03-20 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_browser_app', '0002_author_bookrow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrow',
            name='editions',
            field=models.CharField(max_length=250, verbose_name='Editions'),
        ),
        migrations.AlterField(
            model_name='bookrow',
            name='published_year',
            field=models.CharField(max_length=4, verbose_name='PublishedYear'),
        ),
        migrations.AlterField(
            model_name='bookrow',
            name='raters',
            field=models.CharField(max_length=250, verbose_name='Raters'),
        ),
    ]