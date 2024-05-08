from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Book.Status.PUBLISHED)


class Book(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Отложено'
        PUBLISHED = 1, 'Прочитано'
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг',
                            )
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", default=None, blank=True,
                              null=True, verbose_name='Обложка')
    year = models.IntegerField(blank=True, null=True, verbose_name='Год')
    author = models.CharField(max_length=255, verbose_name='Автор')
    annotation = models.TextField(blank=True, verbose_name='Аннотация')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name='Статус')
    fictions = models.ForeignKey('Fictions', on_delete=models.PROTECT, related_name='book', verbose_name='Жанр')
    tags = models.ManyToManyField('TagBook', blank=True, related_name='tags', verbose_name='Тэг')
    publisher = models.OneToOneField('Publisher', on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='pub_book', verbose_name='Издательство')
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              null=True,
                              default=None)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = "Книги"
        verbose_name_plural = "Книги"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book', kwargs={'book_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Fictions(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Жанр')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')

    objects = models.Manager()

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('fictions', kwargs={'fictions_slug': self.slug})


class TagBook(models.Model):
    tag = models.CharField(max_length=180, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    objects = models.Manager()

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
