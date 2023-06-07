from django.db import models


class Category(models.Model):
    title = models.CharField("Название", max_length=100)

    def count(self):
        return Word.objects.filter(category=self).count()


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
