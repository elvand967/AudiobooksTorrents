# D:\Python\django\AudiobooksTorrents\Audiobooks\torrent\urls.py

from django.urls import path, re_path, register_converter
from torrent import views, converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000/
    path('genres/<slug:genres_slug>/', views.genres, name='genres'),
    path('cat/<int:cat_id>/', views.categories, name='categories'),
    # re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive),
    path('archive/<year4:year>/', views.archive, name='archive'),  # собственный конвертер
]
