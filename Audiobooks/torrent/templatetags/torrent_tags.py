# D:\Python\django\AudiobooksTorrents\Audiobooks\torrent\templatetags\torrent_tags.py

from django import template
import torrent.views as views

# экземпляр класса Library, через который происходит регистрация собственных шаблонных тегов:
register = template.Library()


#  определим функцию def get_horizontal_menu(), которая будет выполняться при вызове нашего тега из шаблона
#  и свяжем эту функцию с тегом, или, превратим эту функцию в тег, используя специальный декоратор,
#  доступный через переменную register:
@register.simple_tag()
def get_horizontal_menu():
    menu = [
        {'title': "О сайте", 'url_name': 'about', 'link_hint': 'О нас, контакты, другая информация'},
        {'title': "FAG", 'url_name': 'about', 'link_hint': 'Часто задаваемые вопросы'},
        {'title': "Обратная связь", 'url_name': 'contact', 'link_hint': 'Отправить сообщение администрации сайта'},
        {'title': "Общий чат", 'url_name': 'general_chat', 'link_hint': 'Войти в общий чат сайта'},
    ]
    return menu


@register.simple_tag(name='getcats')
def get_categories():
    '''Простой пользовательский тэг'''
    return views.cats_db

@register.inclusion_tag('torrent/custom_tag/list_categories.html')
def show_categories(cat_selected=0):
    '''пользовательский включающий тег'''
    cats = views.cats_db
    return {"cats": cats, "cat_selected": cat_selected}