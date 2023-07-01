from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
import logging

from .models import Category, Word
from .serializers import CategoryDetailSerializer, CategoryListSerializer, WordListSerializer


logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    lookup_field = "title"
    lookup_url_kwarg = "category_title"

    def get_serializer(self, *args, **kwargs):
        if self.action == "retrieve":
            return CategoryDetailSerializer(*args, **kwargs)
        else:
            return CategoryListSerializer(*args, **kwargs)

    @action(methods=['get'], detail=True)
    def words(self, request, category_title: str):
        words = Word.objects.filter(category__title=category_title)
        serializer = WordListSerializer(instance=words, many=True)
        return Response(serializer.data)
