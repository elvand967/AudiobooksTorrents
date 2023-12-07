
# Служебные утилиты
import os
from django import setup
# Устанавливаем переменную окружения, указывающую Django, в каком проекте искать настройки
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Audiobooks.settings")
# Настраиваем Django
setup()
import sys
sys.path.append("/")


import re
from django.db import connections, IntegrityError
from torrent.models import ModelBooks, Author, Reader, Cycle, ModelSubcategories, ModelCategories
from django.core.exceptions import ObjectDoesNotExist

def main():
    # Первичная загрузка категорий и жанров
    populate_categories_and_subcategories()

    start_id = 1  # начальный id
    end_id = 99   # конечный id
    books_data = get_books_all_data(start_id, end_id)
    save_books_data(books_data)

    pass


def populate_categories_and_subcategories():
    '''Первичная загрузка категорий и жанров'''
    # Категории
    categories = [
        "Альтернативная история",
        "Аудиоспектакль",
        "Бизнес и обучение",
        "Биографии и мемуары",
        "Боевики, детективы и триллеры",
        "Здоровье и медицина",
        "Мистика и ужасы",
        "Наука и познавательная литература",
        "Семейные и детские",
        "Классика",
        "Фантастика",
        "Философия",
        "Фэнтези и любовь",
        "Эзотерика и религия",
        "На иностранных языках",
        "Другое",
    ]

    for category_name in categories:
        category = ModelCategories.objects.create(name=category_name)
        print(f"Добавлена категория: {category}")

    # Подкатегории
    subcategories_mapping = {
        "Альтернативная история": ["Альтернативная история"],
        "Аудиоспектакль": ["Аудиоспектакль"],
        "Бизнес и обучение": ["Бизнес", "Обучение"],
        "Биографии и мемуары": ["Биографии", "Мемуары"],
        "Боевики, детективы и триллеры": ["Боевики", "Детективы", "Триллеры"],
        "Здоровье и медицина": ["Медицина", "Здоровье", "Психология"],
        "Мистика и ужасы": ["Мистика", "Ужасы"],
        "Наука и познавательная литература": [
            "На иностранных языках",
            "Научно-популярное",
            "Познавательная литература",
            "История",
        ],
        "Семейные и детские": [
            "Для детей",
            "Приключения",
            "Сказки",
            "Семейные",
            "Юмор",
            "Сатира",
        ],
        "Классика": ["Классика", "Поэзия", "Проза", "Роман"],
        "Фантастика": [
            "Попаданцы",
            "Этногенез",
            "Технотьма",
            "Фантастика",
            "Метро 2033",
            "Постапокалипсис",
            "EVE online",
            "S.T.A.L.K.E.R.",
            "Warhammer 40000",
            "LitRPG",
            "S-T-I-K-S",
        ],
        "Философия": ["Философия"],
        "Фэнтези и любовь": ["Любовный роман", "Любовное фэнтези", "Фэнтези"],
        "Эзотерика и религия": ["Эзотерика", "Религия"],
    }

    for category_name, subcategory_names in subcategories_mapping.items():
        category = ModelCategories.objects.get(name=category_name)
        for subcategory_name in subcategory_names:
            subcategory = ModelSubcategories.objects.create(
                category=category, name=subcategory_name
            )
            print(f"Добавлена подкатегория: {subcategory}")


def get_books_all_data(start_id, end_id):
    '''Функция использует курсор базы данных для выполнения SQL-запроса,
    который выбирает все строки из таблицы books_all с id в заданном диапазоне.
    Результат представляет собой список кортежей, где каждый кортеж содержит данные одной строки таблицы. '''
    with connections['database_books'].cursor() as cursor:
        cursor.execute("SELECT * FROM books_all WHERE id BETWEEN %s AND %s", [start_id, end_id])
        columns = [col[0] for col in cursor.description]
        books_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return books_data


def save_books_data(books_data):
    '''Загрузка новых данных из 'db_old' '''
    i = 0  # счетчик итераций
    ii = 0  # счетчик успешных итераций
    iii = 0  # счетчик необработанных исключений
    n = 0  # счетчик пропущенных итераций

    for i, book_data in enumerate(books_data):
        try:
            # Проверяем уникальность id_old
            if ModelBooks.objects.filter(id_old=book_data['id']).exists():
                n += 1
                # print(f"Книга с id_old: {book_data['id']} уже зарегистрирована, пропускаем...")
                continue
            # Проверяем наличие торрент-файла
            elif book_data['torrent'] is None:
                n += 1
                print(f"Для книги с id_old: {book_data['id']} нет торрент-файла, пропускаем...")
                continue
            # Проверяем наличие картинки
            elif book_data['picture'] is None:
                n += 1
                print(f"Для книги с id_old: {book_data['id']} нет загруженной картинки, пропускаем...")
                continue

            # Проверяем и создаем связанных авторов
            authors = book_data.get('author', '').split(', ')
            # from django.core.exceptions import ObjectDoesNotExist
            author_instances = []
            for author_name in authors:
                author_slug = translit_re(author_name)  # Генерируем слаг автора
                try:
                    # Пытаемся найти автора по слагу
                    A = Author.objects.get(slug=author_slug)
                    # Если есть экземпляр модели с таким слагом.
                    author = A.name  # Запомним имя (name) зафиксированное в модели 'Author'
                except ObjectDoesNotExist:
                    # Если автор не найден, приводим имя к требуемому виду
                    author = author_name.title()  # Первую букву каждого слова переводит в верхний регистр, а все остальные в нижний
                try:
                    # Ищем или создаем автора в модели 'Author'
                    author_instance, created = Author.objects.get_or_create(name=author)
                    author_instances.append(author_instance)
                except Exception as e:
                    # Обрабатываем другие возможные исключения, если они возникнут
                    iii += 1  # счетчик необработанных исключений
                    print(f"Ошибка обработки автора: {author_name}: {e}")

            # Проверяем и создаем связанных чтецов
            readers = book_data.get('reading', '').split(', ')
            # from django.core.exceptions import ObjectDoesNotExist
            reader_instances = []
            for reader_name in readers:
                reader_slug = translit_re(reader_name)   # Генерируем слаг чтеца
                try:
                    # Пытаемся найти чтеца по слагу
                    R = Reader.objects.get(slug=reader_slug)
                    # Если есть экземпляр модели с таким слагом.
                    reader = R.name  # Запомним имя зафиксированное в модели 'Reader'
                except ObjectDoesNotExist:
                    # Если чтец не найден, приводим имя к требуемому виду
                    reader = reader_name.title()  # Первую букву каждого слова переводит в верхний регистр, а все остальные в нижний
                try:
                    # Ищем или создаем чтеца в модели 'Reader'
                    reader_instance, created = Reader.objects.get_or_create(name=reader)
                    reader_instances.append(reader_instance)
                except Exception as e:
                    # Обрабатываем другие возможные исключения, если они возникнут
                    iii += 1  # счетчик необработанных исключений
                    print(f"Ошибка обработки чтеца: {reader_name}: {e}")

            # Проверяем и создаем связанный цикл
            cycle_name = book_data.get('cycle', '')
            if not cycle_name:
                cycle_instance = None
            else:
                cycle_slug = translit_re(cycle_name)
                # Пытаемся найти цикл по слагу
                try:
                    cycle_instance = Cycle.objects.get(slug=cycle_slug)
                    # Если цикл найден, обновляем его имя, если оно отличается
                    if cycle_instance.name != cycle_name:
                        cycle_instance.name = cycle_name
                        cycle_instance.save()
                except Cycle.DoesNotExist:
                    # Если цикла с таким слагом нет, создаем новый
                    cycle_instance = Cycle.objects.create(name=cycle_name, slug=cycle_slug)

            # Проверяем и создаем связанные жанры
            genres = book_data.get('genre', '').split(', ')
            genre_instances = []

            for genre_name in genres:
                genre_slug = f'genre_{translit_re(genre_name)}'  # Генерируем слаг Жанра

                try:
                    # Пытаемся найти жанр по слагу
                    genre_instance = ModelSubcategories.objects.get(slug=genre_slug)
                    # Если есть экземпляр модели с таким слагом, добавляем его в список
                    genre_instances.append(genre_instance)

                except ObjectDoesNotExist:
                    try:
                        # Если жанра нет, создаем новый и присваиваем категорию "Другое"
                        other_category, _ = ModelCategories.objects.get_or_create(name="Другое")
                        # Приводим имя к требуемому виду
                        genre_name_capitalized = genre_name.capitalize()
                        # Создаем экземпляр ModelSubcategories
                        new_genre = ModelSubcategories.objects.create(name=genre_name_capitalized,
                                                                      category=other_category)
                        # Добавляем новый жанр в список
                        genre_instances.append(new_genre)

                    except IntegrityError as e:
                        # Обрабатываем ошибку уникальности (если такой жанр был создан другим потоком в то время,
                        # как мы его искали или создавали)
                        # В этом случае, снова пытаемся найти уже созданный жанр
                        genre_instance = ModelSubcategories.objects.get(slug=genre_slug)
                        genre_instances.append(genre_instance)

                    except Exception as e:
                        # Обрабатываем другие возможные исключения, если они возникнут
                        iii += 1  # счетчик необработанных исключений
                        print(f"Ошибка обработки `жанра`: {genre_name}: {e}")

            # Создаем экземпляр ModelBooks
            book_instance = ModelBooks.objects.create(
                id_old=book_data['id'],
                title=book_data['title'],
                # Генерируем уникальный слаг для заголовка и авторов
                slug=f"{translit_re(book_data['title'])}-{translit_re(book_data['author'])}",
                year=book_data["year"],
                duration=book_data['duration'],
                quality=book_data['quality'],
                number_in_cycle=book_data['number_cycle'],
                size=book_data['size'],
                description=book_data['description'],
                folder_torrent_img=book_data['path_torrent'],
                name_torrent=book_data['torrent'],
                name_picture=book_data['picture'],
                like=book_data['like'],
                dislike=book_data['dislike'],
                total_comments=book_data['comments'],
                cycle=cycle_instance,
            )

            # Сохраняем объект ModelBooks, чтобы получить id
            book_instance.save()

            # Добавляем связанных авторов, чтецов и жанры
            book_instance.authors.set(author_instances)
            book_instance.readers.set(reader_instances)
            book_instance.genres.set(genre_instances)

            ii += 1  # счетчик успешных итераций
            print(f"{ii} / {i + 1} ({iii}) | Book with id_old {book_data['id']} successfully saved.")
        except Exception as e:
            iii += 1  # счетчик необработанных исключений
            print(f"{ii} / {i + 1} ({iii}) | Error saving book with id_old {book_data['id']}: {e}")

    print(f'Всего успешно обработано {ii} из {i + 1} записей.')
    print(f'В том числе необработанных исключений {iii} из {i + 1} записей')
    print(f'Пропущено при обработке {n} записей')




def translit_re(input_str):
    ''' Обеспечение транслитерации кириллицы (и другие символы - непотребности) в латиницу,
        re (регулярные выражения):
        Преимущества:
        Гибкость и контроль над процессом транслитерации с использованием регулярных выражений.
        Полный контроль над символами, которые подлежат замене.
        Недостатки:
        Требует более длинного кода, особенно если нужно обработать много разных символов.
        '''
    # Составляем словарь транслитерации для каждого символа
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya', 'ґ': 'g', 'є': 'ie', 'ї': 'i', 'і': 'i',
        'ç': 'c', 'ş': 's', 'ğ': 'g', 'ı': 'i',
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'à': 'a', 'è': 'e', 'é': 'e', 'ê': 'e', 'ô': 'o', 'û': 'u', 'â': 'a',
        'а̑': 'a', 'э̑': 'e', 'и̑': 'i', 'о̑': 'o', 'у̑': 'u', 'ĭ': 'y',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }

    # Добавим символы, подлежащие замене
    translit_dict.update({
        '?': '_', '<': '_', '>': '_', ' ': '_', '~': '_', '@': '_', '"': '_', "'": '_', ':': '_',
        ';': '_', '#': '_', '$': '_', '&': '_', '*': '_', '(': '_', ')': '_', '\\': '_', '|': '_',
        '/': '_', '.': '_',
        '«': '_', '»': '_',
        ',': '_', '!': '_',
        '‐': '-', '−': '-', '–': '-', '—': '-', '-': '-',
    })

    # Заменяем все символы, кроме латинских букв и "-"
    output_str = ''.join([translit_dict.get(char.lower(), char) for char in input_str])

    # Заменяем множественные подчеркивания на одно
    output_str = re.sub('_+', '_', output_str)

    # Удаление подчеркиваний в начале и конце строки
    output_str = output_str.strip('_')

    # Заменяем множественные дефисы на одно
    output_str = re.sub('-+', '-', output_str)

    # Удаление дефисов в начале и конце строки
    output_str = output_str.strip('-')

    return output_str.lower()


if __name__ == "__main__":
    main()