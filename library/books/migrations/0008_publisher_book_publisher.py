# Generated by Django 4.2.1 on 2024-02-08 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_tagbook_alter_book_fictions_book_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pub_book', to='books.publisher'),
        ),
    ]