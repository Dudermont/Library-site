# Generated by Django 4.2.1 on 2024-02-07 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_book_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Отложено'), (1, 'Прочитано')], default=0),
        ),
    ]
