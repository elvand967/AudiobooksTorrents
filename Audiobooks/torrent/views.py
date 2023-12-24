# D:\Python\django\AudiobooksTorrents\Audiobooks\torrent\views.py

from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.defaultfilters import slugify


cats_db = [
    {'id': 1, 'name': 'Альтернативная история', 'slug': 'alternativnaya_istoriya'},
    {'id': 2, 'name': 'Аудиоспектакль', 'slug': 'audiospektakl'},
    {'id': 3, 'name': 'Бизнес и обучение', 'slug': 'biznes_i_obuchenie'},
    {'id': 4, 'name': 'Биографии и мемуары', 'slug': 'biografii_i_memuary'},
    {'id': 5, 'name': 'Боевики, детективы и триллеры', 'slug': 'boeviki_detektivy_i_trillery'},
    {'id': 6, 'name': 'Здоровье и медицина', 'slug': 'zdorove_i_meditsina'},
    {'id': 7, 'name': 'Мистика и ужасы', 'slug': 'mistika_i_uzhasy'},
    {'id': 8, 'name': 'Наука и познавательная литература', 'slug': 'nauka_i_poznavatelnaya_literatura'},
    {'id': 9, 'name': 'Семейные и детские', 'slug': 'semeynye_i_detskie'},
    {'id': 10, 'name': 'Классика', 'slug': 'klassika'},
    {'id': 11, 'name': 'Фантастика', 'slug': 'fantastika'},
    {'id': 12, 'name': 'Философия', 'slug': 'filosofiya'},
    {'id': 13, 'name': 'Фэнтези и любовь', 'slug': 'fentezi_i_lyubov'},
    {'id': 14, 'name': 'Эзотерика и религия', 'slug': 'ezoterika_i_religiya'},
    {'id': 15, 'name': 'На иностранных языках', 'slug': 'na_inostrannykh_yazykakh'},
    {'id': 16, 'name': 'Другое', 'slug': 'drugoe'},
]

data_db = [
    {'id': 1, 'title': 'Не считая собаки', 'author': 'Уиллис Конни', 'genre': 'Попаданцы, Фантастика, фэнтези',
     'description': '''Нед Генри честный труженик и вынужден так тяжело и много работать, что не редко готов заснуть на ходу, потому что крайне нуждается в отдыхе.
    Работёнка досталась и впрямь нелёгкая, приходится постоянно перемещаться из XXI века в 1940 год и обратно, чтобы
    поддерживать проект реконструкции собора в английском городе Ковентри, пострадавшего от бомбардировки
    немецко - фашистской авиацией в ходе II Мировой войны.

    Положение становится ещё труднее и опаснее после того, как отважная Верити Киндл приволокла из прошлого ещё
    кое - что.
    Она такой же путешественник во времени, но проявила недопустимую оплошность.Неду теперь предстоит спешно
    возвращаться в викторианский период.

    Надо срочно вернуть всё на место.
    В противном случае весь проект погибнет, а изменения истории приведут к гибельным последствиям.''',
     'is_published': True},
    {'id': 2, 'title': 'Сделка с демоном', 'author': 'Кардашов Андрей', 'genre': 'Фантастика, фэнтези',
     'description': '''Рыцари Светлого Ордена много лет сражаются с силами зла. 
    И вот наконец им удаётся победить высшего демона и отправить его в Нижний мир. 

    Но это не стало окончанием их борьбы. 
    В рядах рыцарей оказался гнусный предатель, соблазнившийся на посулы демона. 
    Этот негодяй принялся хладнокровно убивать своих товарищей поодиночке, оставаясь неизвестным для них. 

    Оставшимся в живых необходимо понять, кто в их рядах стал предателем, изменив рыцарскому долгу. 
    Если этого не выяснить вовремя, то потом станет слишком поздно.''', 'is_published': False},
    {'id': 3, 'title': '11/22/63', 'author': 'Кинг Стивен', 'genre': 'Детективы, триллеры, Фантастика, фэнтези',
     'description': '''Этот роман культового и весьма плодовитого американского писателя многие считают лучшим в числе его многочисленных произведений. 
    Причём в этом сходятся мнения и рядовых читателей и маститых профессиональных литературных критиков. 

    В основе сюжета попытка спасти президента Джона Кеннеди. 

    Его убийство явилось одним из наиболее драматичных событий истории США в XX столетии. 
    Обыкновенный учитель из маленького провинциального городка Джейк Эппинг получает возможность перемещаться во времени между эпохами и решает воспользоваться этой возможностью для предотвращения убийства лидера страны. 
    Какую цену за это приходится заплатить''', 'is_published': False},
    {'id': 4, 'title': 'Питер. Вселенная метро 2033', 'author': 'Врочек Шимун',
     'genre': 'Метро 2033, Постапокалипсис, Фантастика, фэнтези',
     'description': '''"Метро 2033" Дмитрия Глуховского - культовый фантастический роман, самая обсуждаемая российская книга последних лет. 

    Тираж - полмиллиона, переводы на десятки языков плюс грандиозная компьютерная игра! 
    Эта постапоклиптическая история вдохновила целую плеяду современных писателей, и теперь они вместе создают "Вселенную Метро 2033", серию книг по мотивам знаменитого романа. 
    
    Герои этих новых историй наконец-то выйдут за пределы Московского метро. 
    Их приключения на поверхности Земли, почти уничтоженной ядерной войной, превосходят все ожидания. 
    
    Теперь борьба за выживание человечества будет вестись повсюду!''', 'is_published': False},
    {'id': 5, 'title': 'Дочь воина, или Кадеты не сдаются', 'author': 'Звёздная Елена', 'genre': 'Любовное фэнтези',
     'description': '''Киран МакВаррас – кадет первого курса Космического университета. 

    Она уверена, что жизнь создана для приключений, и не теряет времени даром. 
    В перерывах между занятиями в лучшем учебном заведении героиня участвует в опасных гонках, подделывает удостоверения и ходит в букмекерскую контору.
    Но внезапно в жизни восемнадцатилетней девушки появляются новые обстоятельства. 
    
    Оказывается, что она вовсе не отчаянный кадет, а принцесса Иристана, и теперь вместо совершения проделок и самоволок ей придется возглавить государство и выйти замуж за сильнейшего воина. 
    Находчивая Киран не собирается подчиняться воле отца, но древние знания симбионтов Иристана откроют перед ней мир, полный тайн и магии.''',
     'is_published': True},
]


def index(request):
    # user = request.user
    data = {
        'title': 'Аудиокниги с книжной полки',
        'books': data_db,
        'cat_selected': 0,   # не обязательная строчка
        # 'user': user,
    }
    return render(request, 'torrent/index.html', context=data)


def about(request):
    data = {
        'title': 'О сайте',
        'text': 'На этой странице информация о сайте',
    }
    return render(request, 'torrent/about.html', context=data)


def fag(request):
    data = {
        'title': 'FAG',
        'text': 'Часто задаваемые вопросы',
    }
    return render(request, 'torrent/fag.html', context=data)

def feedback(request):
    data = {
        'title': 'Обратная связь',
        'text': 'Здесь должна быть форма обратной связи',
    }
    return render(request, 'torrent/feedback.html', context=data)


def chat(request):
    data = {
        'title': 'Общий чат',
        'text': 'Общий чат сайта',
    }
    return render(request, 'torrent/chat.html', context=data)


def details(request, det_id):
    return HttpResponse(f"Отображение описания книги с id = {det_id}")


def categories(request, cat_slug):
    return HttpResponse(f"<h1>Категории книг</h1><br><p>Выбрана<h2>slug:{cat_slug}</h2></p>")


def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'torrent/index.html', context=data)


def genres(request, genres_slug):
    if request.POST:
        print(request.POST)
    return HttpResponse(f"<h1>Жанры книг</h1><br><p>Выбран жанр:<h2>{genres_slug}</h2></p>")


def archive(request, year):
    if year > 2023:
        url_redirect = reverse('genres', args=('genre_biznes',))
        return HttpResponsePermanentRedirect(url_redirect,
                                             True)  # постоянное перенаправление на страницу жанра 'genre_biznes'
    return HttpResponse(f"<h1>Архив по годам</h1><h2>{year}</h2>")


class FourDigitYearConverter:
    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')









def login(request):
    data = {
        'title': 'Вход',
        'text': 'Форма входа',
    }
    return render(request, 'torrent/account/login.html', context=data)


def register_user(request):
    data = {
        'title': 'Профиль',
        'text': 'Профиль пользователя',
    }
    return render(request, 'torrent/account/register.html', context=data)

def profile(request):
    data = {
        'title': 'Профиль',
        'text': 'Профиль пользователя',
    }
    return render(request, 'torrent/account/profile.html', context=data)