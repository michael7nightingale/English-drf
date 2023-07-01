from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField("Название", max_length=100)

    def count(self):
        return Word.objects.filter(category=self).count()

    def get_absolute_url(self) -> str:
        return reverse("category_detail", kwargs={"categories_title": self.title})

    def __str__(self):
        return self.title


class Word(models.Model):
    word = models.CharField("Слово", max_length=150)
    translate = models.CharField("Перевод", max_length=200)
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.word
