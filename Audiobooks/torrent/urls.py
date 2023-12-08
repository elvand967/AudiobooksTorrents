# D:\Python\django\AudiobooksTorrents\Audiobooks\torrent\urls.py

from django.urls import path
from torrent.views import index, categories, genres

urlpatterns = [
    path('', index),  # http://127.0.0.1:8000/
    path('cat/', categories),
    path('genres/', genres)
]
