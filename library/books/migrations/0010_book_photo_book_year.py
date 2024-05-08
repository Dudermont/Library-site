# Generated by Django 4.2.1 on 2024-03-19 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_uploadfiles_alter_book_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d', verbose_name='Обложка'),
        ),
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Год'),
        ),
    ]