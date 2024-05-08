from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Book, Fictions, TagBook, UploadFiles
from .utils import DataMixin


class BookHome(DataMixin, ListView):
    template_name = 'books/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    fict_selected = 0

    def get_queryset(self):
        return Book.published.all().select_related('fictions')


@login_required
def about(request):
    contact_list = Book.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,
                  'books/about.html',
                  {'title': 'О нас', 'page_obj': page_obj})


class AddBook(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'books/addbook.html'
    title_page = 'Добавление книги'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.owner = self.request.user
        return super().form_valid(form)


class UpdateBook(DataMixin, UpdateView):
    model = Book
    fields = ['title', 'annotation', 'photo', 'is_published', 'fictions']
    template_name = 'books/addbook.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование книги'


def contact(request):
    return HttpResponse(f"Обратная связь")


def login(request):
    return HttpResponse(f"Авторизация")


class BookFiction(DataMixin, ListView):
    template_name = 'books/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Book.published.filter(fictions__slug=self.kwargs['fictions_slug']).select_related('fictions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fictions = context['posts'][0].fictions
        return self.get_mixin_context(context,
                                      title='Жанр - ' + fictions.name,
                                      fict_selected=fictions.pk,
                                      )


class ShowBook(DataMixin, DetailView):
    # model = Book
    template_name = 'books/book.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['posts'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Book.published, slug=self.kwargs[self.slug_url_kwarg])


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagBooklist(DataMixin, ListView):
    template_name = 'books/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Book.published.filter(tags__slug=self.kwargs['tag_slug']).prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = context['posts'][0].tags.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тэг: ' + tag.tag)
