from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField("Название", max_length=100)

    def count(self):
        return Word.objects.filter(category=self).count()

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"category_name": self.title})

    def __str__(self):
        return self.title


class Word(models.Model):
    word = models.CharField("Слово", max_length=150)
    translate = models.CharField("Перевод", max_length=200)
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE)


class BaseTextMessage(models.Model):
    text = models.TextField("Текст сообщения", max_length=1000)
    date = models.DateTimeField("Время сообщения", auto_now=True)

    class Meta:
        abstract = True


class Message(BaseTextMessage):

    class TypeChoices(models.TextChoices):
        remark = ("remark", "Remark")
        pupil = ("pupil", 'Pupil')

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    reply_to = models.OneToOneField('Message', on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField("Тип сообщения", max_length=100, default="remark",
                            choices=TypeChoices.choices)
