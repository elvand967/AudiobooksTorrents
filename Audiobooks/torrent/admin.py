# D:\Python\django\AudiobooksTorrents\Audiobooks\torrent\admin.py

from django.contrib import admin
from .models import ModelCategories, ModelSubcategories, Author, Reader, Cycle, ModelBooks, UserBookRating, CriteriaRating, BookAverageRating, Comment, Reply

# Регистрация моделей в админ-панели
@admin.register(ModelCategories)
class ModelCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ModelSubcategories)
class ModelSubcategoriesAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ModelBooks)
class ModelBooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'year', 'time_create', 'time_update', 'is_published')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(UserBookRating)
class UserBookRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'like')

@admin.register(CriteriaRating)
class CriteriaRatingAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'plot', 'writing_talent', 'characters', 'voice_quality', 'created_at', 'updated_at')

@admin.register(BookAverageRating)
class BookAverageRatingAdmin(admin.ModelAdmin):
    list_display = ('book', 'plot', 'writing_talent', 'characters', 'voice_quality', 'total_ratings')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'text', 'created_at', 'updated_at')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'text', 'created_at', 'updated_at')

