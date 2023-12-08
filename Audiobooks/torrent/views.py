# D:\Python\django\AudiobooksTorrents\Audiobooks\torrent\views.py

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Страница приложения torrent.")


def categories(request):
    return HttpResponse("<h1>Категории книг</h1>")


def genres(request):
    return HttpResponse("<h1>Жанры книг</h1>")