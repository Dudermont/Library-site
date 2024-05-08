# Generated by Django 4.2.1 on 2024-02-08 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_book_fictions'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(db_index=True, max_length=180)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='fictions',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='book', to='books.fictions'),
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='books.tagbook'),
        ),
    ]
