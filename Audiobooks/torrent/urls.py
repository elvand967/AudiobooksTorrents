# D:\Python\django\AudiobooksTorrents\Audiobooks\torrent\urls.py

from django.urls import path, re_path, register_converter
from torrent import views, converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000/
    path('about/', views.about, name='about'),
    path('fag/', views.fag, name='fag'),
    path('feedback/', views.feedback, name='feedback'),
    path('chat/', views.chat, name='chat'),
    path('login/', views.login, name='login'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.index, name='logout'),



    # path('contact/', views.contact, name='contact'),
    path('details/<int:det_id>/', views.details, name='details'),
    path('genres/<slug:genres_slug>/', views.genres, name='genres'),
    path('cat/<slug:cat_slug>/', views.categories, name='categories'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
    # re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive),
    path('archive/<year4:year>/', views.archive, name='archive'),  # собственный конвертер
]
