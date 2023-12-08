# D:\Python\django\AudiobooksTorrents\Audiobooks\Audiobooks\urls.py

"""Конфигурация URL-адреса аудиокниг

Список `urlpatterns` направляет URL-адреса в представления. Для получения дополнительной информации см.:
     https://docs.djangoproject.com/en/4.1/topics/http/urls/
Примеры:
Представления функций
     1. Добавьте импорт: из представлений импорта my_app.
     2. Добавьте URL-адрес в urlpatterns: path('',views.home, name='home')
Представления на основе классов
     1. Добавляем импорт: fromother_app.views import Home
     2. Добавьте URL-адрес в urlpatterns: path('', Home.as_view(), name='home')
Включение другого URLconf
     1. Импортируйте функцию include(): из django.urls import include, путь
     2. Добавьте URL-адрес в urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('torrent.urls')),
]



# процесс необходим для работы в отладочном режиме
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)