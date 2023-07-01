from django.contrib import admin

from .models import Word, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("id", "word", 'category')
