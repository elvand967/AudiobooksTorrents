
# D:\Python\django\AudiobooksTorrents\Audiobooks\torrent\models.py
import os

from django.db import models
from django.dispatch import receiver

from django.urls import reverse
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.utils.text import slugify

from .utilities import translit_re, get_torrent_file_path, get_picture_file_path
from django.conf import settings
media_root = settings.MEDIA_ROOT


class ModelCategories(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        # Генерируем уникальный слаг для категории
        self.slug = translit_re(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class ModelSubcategories(models.Model):
    category = models.ForeignKey(ModelCategories, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Категория")
    name = models.CharField(max_length=100, db_index=True, verbose_name="Жанр")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        # Генерируем уникальный слаг для подкатегории
        self.slug = f'genre_{translit_re(self.name)}'
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.category} - {self.name}"

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={'cat_slug': self.category.slug, 'subcat_slug': self.slug})

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['id']


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        # Генерируем уникальный слаг
        self.slug = translit_re(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.name}"

    def get_absolute_url(self):
        return reverse('author', kwargs={'author_slug': self.slug})

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Reader(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        # Генерируем уникальный слаг
        self.slug = translit_re(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.name}"

    def get_absolute_url(self):
        return reverse('reader', kwargs={'reader_slug': self.slug})

    class Meta:
        verbose_name = 'Чтец'
        verbose_name_plural = 'Чтецы'


class Cycle(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, null=True, verbose_name="Описание цикла")

    def save(self, *args, **kwargs):
        # Генерируем уникальный слаг
        self.slug = translit_re(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.name}"

    def get_absolute_url(self):
        return reverse('cycle', kwargs={'cycle_slug': self.name})

    class Meta:
        verbose_name = 'Цикл'
        verbose_name_plural = 'Циклы'





class ModelBooks(models.Model):
    id_old = models.IntegerField(unique=True, null=True, blank=True, verbose_name="id_old")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    authors = models.ManyToManyField(Author, blank=True, verbose_name="Авторы")
    readers = models.ManyToManyField(Reader, blank=True, verbose_name="Чтецы")
    year = models.IntegerField(null=True, blank=True, verbose_name="Год",)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    duration = models.CharField(max_length=255, verbose_name="Продолжительность")
    quality = models.CharField(max_length=255, verbose_name="Качество")
    cycle = models.ForeignKey(Cycle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Цикл")
    number_in_cycle = models.IntegerField(null=True, blank=True, verbose_name="Номер в цикле")
    size = models.CharField(null=True, blank=True, max_length=255, verbose_name="Размер")
    genres = models.ManyToManyField('ModelSubcategories', blank=False, default=None, verbose_name="Жанры")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    folder_torrent_img = models.CharField(max_length=255, verbose_name="Директория расположения файла")
    name_torrent = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя Торрент-файла")
    torrent = models.FileField(upload_to=get_torrent_file_path, blank=True, null=True, verbose_name="Торрент")
    name_picture = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя файла картинки")
    picture = models.ImageField(upload_to=get_picture_file_path, blank=True, null=True, verbose_name="Картинка")
    like = models.IntegerField(default=0, verbose_name="Нравится(+)")
    dislike = models.IntegerField(default=0, verbose_name="Не нравится(-)")
    total_comments = models.IntegerField(default=0, verbose_name="Всего комментариев")
    is_published = models.BooleanField(default=False, verbose_name="Публикация")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book', kwargs={'book_slug': self.slug})

    def save(self, *args, **kwargs):
        # Приозведена загрузка из db_old
        if self.id_old:
            # формируем имя вложенных директорий
            self.subdirectory = str(self.id_old // 1000)

            # Формируем путь для торрент-файла если его нет
            if self.name_torrent and not self.torrent:
                torrent_path = os.path.join('files_torrent', self.subdirectory, self.name_torrent)
                if os.path.exists(os.path.join(media_root, torrent_path)):
                    self.torrent = torrent_path

            # Формируем путь для файла-картинки если его нет
            if self.name_picture and not self.picture:
                picture_path = os.path.join('files_picture', self.subdirectory, self.name_picture)
                if os.path.exists(os.path.join(media_root, picture_path)):
                    self.picture = picture_path

        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     # Приозведена загрузка из db_old
    #     if self.id_old:
    #         # формируем имя вложенных директорий
    #         self.subdirectory = str(self.id_old//1000)
    #
    #         # Формируем путь для торрент-файла если его нет
    #         if self.name_torrent and not self.torrent:
    #             torrent_path = os.path.join('folder_files\\files_torrent', self.subdirectory, self.name_torrent)
    #             if os.path.exists(torrent_path):
    #                 self.torrent = torrent_path
    #
    #         # Формируем путь для файла-картинки если его нет
    #         if self.name_picture and not self.picture:
    #             picture_path = os.path.join('folder_files\\files_picture', self.subdirectory, self.name_picture)
    #             if os.path.exists(picture_path):
    #                 self.picture = picture_path
    #
    #     super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Аудиокнига'
        verbose_name_plural = 'Аудиокниги'  # уточнить названия
        ordering = ['-year', 'title']  # сортировка по дате убывания


class UserBookRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_ratings', verbose_name="Пользователь")
    book = models.ForeignKey(ModelBooks, on_delete=models.CASCADE, related_name='user_ratings', verbose_name="Книга")
    like = models.BooleanField(verbose_name="Лайк", default=False)

    class Meta:
        unique_together = ['user', 'book']  # Гарантирует уникальность комбинации пользователя и книги


@receiver(post_save, sender=UserBookRating)
@receiver(post_delete, sender=UserBookRating)
def update_book_likes_dislikes(sender, instance, **kwargs):
    book = instance.book
    book.like = book.user_ratings.filter(like=True).count()
    book.dislike = book.user_ratings.filter(like=False).count()
    book.save()


# регистрация сигнала
post_save.connect(update_book_likes_dislikes, sender=UserBookRating)
post_delete.connect(update_book_likes_dislikes, sender=UserBookRating)

''' Модель для хранения оценок пользователей 
по каждому из критериев (Сюжет, Писательский талант, Персонажи, Качество голоса) '''
class CriteriaRating(models.Model):
    book = models.ForeignKey(ModelBooks, on_delete=models.CASCADE, related_name='criteria_ratings', verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_criteria_ratings', verbose_name="Пользователь")
    plot = models.IntegerField(default=0, verbose_name="Сюжет")
    writing_talent = models.IntegerField(default=0, verbose_name="Писательский талант")
    characters = models.IntegerField(default=0, verbose_name="Персонажи")
    voice_quality = models.IntegerField(default=0, verbose_name="Качество голоса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        unique_together = ['user', 'book']  # Гарантирует уникальность комбинации пользователя и книги


@receiver(post_save, sender=CriteriaRating)
@receiver(post_delete, sender=CriteriaRating)
def update_criteria_ratings(sender, instance, **kwargs):
    book = instance.book
    average_rating, created = BookAverageRating.objects.get_or_create(book=book)
    average_rating.update_average_ratings()


# Регистрация сигналов для оценок критериев
post_save.connect(update_criteria_ratings, sender=CriteriaRating)
post_delete.connect(update_criteria_ratings, sender=CriteriaRating)


''' Средние оценки по книге '''
class BookAverageRating(models.Model):
    book = models.OneToOneField(ModelBooks, on_delete=models.CASCADE, related_name='average_rating', verbose_name="Книга")
    plot = models.FloatField(default=0.0, verbose_name="Сюжет")
    writing_talent = models.FloatField(default=0.0, verbose_name="Писательский талант")
    characters = models.FloatField(default=0.0, verbose_name="Персонажи")
    voice_quality = models.FloatField(default=0.0, verbose_name="Качество голоса")
    total_ratings = models.IntegerField(default=0, verbose_name="Общее количество оценок")

    def update_average_ratings(self):
        criteria_ratings = CriteriaRating.objects.filter(book=self.book)
        total_ratings = criteria_ratings.count()

        if total_ratings == 0:
            # Если нет оценок, оставляем средние оценки без изменений
            pass
        else:
            # Обновляем только при изменении
            if self.total_ratings != total_ratings:
                self.total_ratings = total_ratings
                self.save()

            # Обновляем средние оценки
            self.plot = sum(rating.plot for rating in criteria_ratings) / total_ratings
            self.writing_talent = sum(rating.writing_talent for rating in criteria_ratings) / total_ratings
            self.characters = sum(rating.characters for rating in criteria_ratings) / total_ratings
            self.voice_quality = sum(rating.voice_quality for rating in criteria_ratings) / total_ratings

        self.save()


@receiver(post_save, sender=BookAverageRating)
@receiver(post_delete, sender=BookAverageRating)
def update_average_ratings(sender, instance, **kwargs):
    book = instance.book
    criteria_ratings = CriteriaRating.objects.filter(book=book)
    total_ratings = criteria_ratings.count()

    if total_ratings > 0:
        instance.plot = sum(rating.plot for rating in criteria_ratings) / total_ratings
        instance.writing_talent = sum(rating.writing_talent for rating in criteria_ratings) / total_ratings
        instance.characters = sum(rating.characters for rating in criteria_ratings) / total_ratings
        instance.voice_quality = sum(rating.voice_quality for rating in criteria_ratings) / total_ratings
        instance.total_ratings = total_ratings
    else:
        # Если нет оценок, сбрасываем средние оценки
        instance.plot = 0.0
        instance.writing_talent = 0.0
        instance.characters = 0.0
        instance.voice_quality = 0.0
        instance.total_ratings = 0

    instance.save()


# Регистрация сигналов для средних оценок
post_save.connect(update_average_ratings, sender=BookAverageRating)
post_delete.connect(update_average_ratings, sender=BookAverageRating)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Пользователь")
    book = models.ForeignKey(ModelBooks, on_delete=models.CASCADE, related_name='book_comments', verbose_name="Книга")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.book.title}"

    class Meta:
        ordering = ['created_at']


@receiver(post_save, sender=Comment)
def update_comments_count(sender, instance, **kwargs):
    instance.book.comments = Comment.objects.filter(book=instance.book).count()
    instance.book.save()


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies', verbose_name="Пользователь")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', verbose_name="Комментарий")
    text = models.TextField(verbose_name="Текст ответа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Reply by {self.user.username} on {self.comment.book.title}"

    class Meta:
        ordering = ['created_at']


@receiver(post_save, sender=Reply)
def update_comments_count(sender, instance, **kwargs):
    instance.comment.book.comments = Comment.objects.filter(book=instance.comment.book).count()
    instance.comment.book.save()