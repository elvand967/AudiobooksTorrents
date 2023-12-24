# D:\Python\django\AudiobooksTorrents\Audiobooks\torrent\templatetags\torrent_tags.py

from django import template
from django.http import request

# import torrent.views as views

'''экземпляр класса Library,
через который происходит регистрация собственных шаблонных тегов:'''
register = template.Library()



@register.simple_tag(name='horizontal_menu')
def get_horizontal_menu():
    '''Функция def get_horizontal_menu(), которая будет возвращать
    список ссылок главного меню при вызове нашего тега из шаблона.
    Свяжем эту функцию с тегом, или, превратим эту функцию в тег, используя специальный декоратор
    `@register.simple_tag(name='horizontal_menu')`,
     доступный через переменную `register`.  '''
    menu = [
        {'title': "Главная", 'url_name': 'home', 'link_hint': 'Аудиокниги с книжной полки'},
        {'title': "О нас", 'url_name': 'about', 'link_hint': 'О нас, контакты, другая информация'},
        {'title': "FAG", 'url_name': 'fag', 'link_hint': 'Часто задаваемые вопросы'},
        {'title': "Обратная связь", 'url_name': 'feedback', 'link_hint': 'Отправить сообщение администрации сайта'},
        {'title': "Чат", 'url_name': 'chat', 'link_hint': 'Войти в общий чат сайта'},
    ]
    return menu


@register.simple_tag(name='menu_users')
def get_users_menu(user):
    '''Функция def get_users_menu(), которая будет возвращать
    список ссылок входа, регистрации, профиля и выхода пользователя при вызове нашего тега из шаблона.
    Свяжем эту функцию с тегом, или, превратим эту функцию в тег, используя специальный декоратор
    `@register.simple_tag(name='menu_users')`,
     доступный через переменную `register`.  '''
    # menu = [
    #     {'title': "Вход", 'url_name': 'login', 'link_hint': 'Войти на сайт'},
    #     {'title': "Регистрация", 'url_name': 'about', 'link_hint': 'О нас, контакты, другая информация'},
    #     {'title': "Профиль", 'url_name': 'profile', 'link_hint': 'Профиль пользователя'},
    #     {'title': "Выход", 'url_name': 'home', 'link_hint': 'Выход пользователя'},
    # ]
    # user = request.user
    if user.is_authenticated:
        menu = [
            {'title': "Профиль", 'url_name': 'profile', 'link_hint': 'Профиль пользователя'},
            {'title': "Выход", 'url_name': 'logout', 'link_hint': 'Выход пользователя'},
        ]
    else:
        menu = [
            {'title': "Вход", 'url_name': 'login', 'link_hint': 'Войти на сайт'},
            {'title': "Регистрация", 'url_name': 'register', 'link_hint': 'Регистрация на сайте'},
        ]

    return menu


# @register.simple_tag(name='getcats')
# def get_categories():
#     '''Простой пользовательский тэг'''
#     return views.cats_db
#
# @register.inclusion_tag('torrent/custom_tag/list_categories.html')
# def show_categories(cat_selected=0):
#     '''пользовательский включающий тег'''
#     cats = views.cats_db
#     return {"cats": cats, "cat_selected": cat_selected}