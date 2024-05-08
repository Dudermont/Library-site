from django import template
from django.db.models import Count

import books.views as views
from books.models import Fictions, TagBook

register = template.Library()


@register.inclusion_tag('books/list_fiction.html')
def show_fiction(fict_selected=0):
    ficts = Fictions.objects.annotate(total=Count('book')).filter(total__gt=0)
    return {'ficts': ficts, 'fict_selected': fict_selected}


@register.inclusion_tag('books/list_tags.html')
def show_all_tags():
    return {'tags': TagBook.objects.annotate(total=Count('tags')).filter(total__gt=0)}
