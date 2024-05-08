menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить книгу", 'url_name': 'addbook'},
    {'title': "Обратная связь", 'url_name': 'contact'},
]


class DataMixin:
    paginate_by = 3
    title_page = None
    fict_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.fict_selected is not None:
            self.extra_context['fict_selected'] = self.fict_selected

    def get_mixin_context(self, contex, **kwargs):
        contex['fict_selected'] = None
        contex.update(kwargs)
        return contex
