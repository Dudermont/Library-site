from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Fictions, Publisher, Book


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские буквы"

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    fictions = forms.ModelChoiceField(queryset=Fictions.objects.all(), empty_label="Жанр не выбран", label="Жанр")
    publisher = forms.ModelChoiceField(queryset=Publisher.objects.all(), required=False, empty_label="Самиздат", label="Издатель")

    class Meta:
        model = Book
        fields = ['title', 'slug', 'author', 'annotation', 'photo', 'is_published', 'fictions', 'publisher', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'annotation': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 30:
            raise ValidationError("Длинна превышает допустимый предел")

        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")
