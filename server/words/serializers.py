from rest_framework import serializers

from .models import Category, Word


class WordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ("word", "translate")


class CategoryListSerializer(serializers.ModelSerializer):
    words = WordListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'get_absolute_url', "count", 'words')


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "get_absolute_url")
