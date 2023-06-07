from django.contrib import admin

from .models import Message, Word, Category


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date')
    list_display_links = ('id', 'user', 'date')


@admin.register(Category)
class CategoryResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


@admin.register(Word)
class WordCategory(admin.ModelAdmin):
    list_display = ('id', 'word', 'translate', 'category')
    list_display_links = ('id', 'word', 'translate')
