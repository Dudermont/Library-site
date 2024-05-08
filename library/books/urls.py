from django.urls import path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.BookHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addbook/', views.AddBook.as_view(), name='addbook'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:book_slug>/', views.ShowBook.as_view(), name='book'),
    path('fiction/<slug:fictions_slug>/', views.BookFiction.as_view(), name='fictions'),
    path('tag/<slug:tag_slug>/', views.TagBooklist.as_view(), name='tag'),
    path('edit/<int:pk>/', views.UpdateBook.as_view(), name='edit_book'),
]
