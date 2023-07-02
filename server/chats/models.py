from django.db import models

from services.models import UUIDModel


class Chat(UUIDModel):
    account = models.OneToOneField("users.Account", on_delete=models.CASCADE, related_name="chat")

    objects = models.Manager()

    def __str__(self):
        return self.id


class BaseTextMessage(models.Model):
    text = models.TextField("Текст сообщения", max_length=1000)
    time_send = models.DateTimeField("Время сообщения", auto_now=True)

    class Meta:
        abstract = True


class Message(BaseTextMessage):

    class TypeChoices(models.TextChoices):
        remark = ("remark", "Remark")
        pupil = ("pupil", 'Pupil')

    sender = models.ForeignKey("users.Account", on_delete=models.CASCADE)
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE, related_name="chat")
    type = models.CharField("Тип сообщения", max_length=100, default="remark", choices=TypeChoices.choices)

    objects = models.Manager()

    def __str__(self):
        return self.text
