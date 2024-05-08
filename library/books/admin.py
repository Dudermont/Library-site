from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Book, Fictions


class PublisherFilter(admin.SimpleListFilter):
    title = 'Издавался'
    parameter_name = 'status'

    def lookups(self, request, queryset):
        return [
            ('publisher', 'Издательство'),
            ('serlf_publisher', 'Самиздат')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'publisher':
            return queryset.filter(publisher__isnull=False)
        elif self.value() == 'serlf_publisher':
            return queryset.filter(publisher__isnull=True)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'annotation', 'photo', 'book_photo', 'fictions', 'tags']
    readonly_fields = ['book_photo']
    filter_horizontal = ['tags']
    list_display = ('title', 'book_photo', 'time_create', 'is_published', 'fictions')
    list_display_links = ('title', )
    ordering = ['time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 6
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'fictions__name']
    list_filter = [PublisherFilter, 'fictions__name', 'is_published']
    save_on_top = True

    @admin.display(description="Обложка", ordering='annotation')
    def book_photo(self, book: Book):
        if book.photo:
            return mark_safe(f"<img src='{book.photo.url}' width=50")
        return "Без фото"

    @admin.action(description="Опубликовать книгу")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Book.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description="Снять с публикации")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Book.Status.DRAFT)
        self.message_user(request, f" {count} записей сняты с публикации!", messages.WARNING)


@admin.register(Fictions)
class FictionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

