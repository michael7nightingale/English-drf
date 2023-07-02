from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
import logging

from services.models import UUIDModel
from chats.models import Chat


logger = logging.getLogger(__name__)


class CustomUserManager(UserManager):
    def get(self, *args, **kwargs):
        return (
            super()
            .select_related("account")
            .get(*args, **kwargs)
        )


class User(AbstractUser, UUIDModel):
    objects = CustomUserManager()


class AccountManager(models.Manager):
    def create_account(
            self,
            user: dict,
            location: str,
            avatar=None,
    ):
        user = User.objects.create_user(**user)
        user.is_active = False    # for email activation
        user.save()
        account = Account.objects.create(
            location=location,
            avatar=avatar,
            user=user
        )
        account.save()
        # chat_gpt_account = Account.objects.get(user__username='chat-gpt')
        Chat.objects.create(
            account=account,
        )
        return account

    def create_chatgpt_account(
            self,
            user: dict | None = None,
            level: str = "C2",
            score: int = 6000,
            location: str = "NewYork"
    ):
        user = {"username": 'chat-gpt',
                'password': 'chat-gpt-password',
                "email": 'chat_gpt@mail.ru'} if user is None else user

        user = User.objects.create_user(**user)
        account = Account.objects.create(
            location=location,
            level=level,
            score=score,
            user=user
        )
        account.save()
        return account


SCORES = {
    1000: "A1",
    2000: "A2",
    3000: "B1",
    4000: "B2",
    5000: "C1",
    6000: "C2"
}


class Account(UUIDModel):

    class Levels(models.TextChoices):
        A1 = ("A1", "(А1) – начальный")
        A2 = ("A2", "(А2) – ниже среднего")
        B1 = ("B1", "(В1) – средний")
        B2 = ("B2", "(В2) – выше среднего")
        C1 = ("C1", "(C1) – продвинутый")
        C2 = ("C2", "(C2) – профессиональный уровень владения")

    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    location = models.CharField("Location", max_length=200)
    avatar = models.ImageField("Avatar", upload_to='uploads/avatars/', null=True, blank=True)
    level = models.CharField("Уровень английского", max_length=100, default='A1')
    score = models.IntegerField("Очки английского", null=True, default=0, blank=True)
    # need_exam = models.BooleanField(default=False)

    objects = AccountManager()

    def add_score(self, score: int) -> None:
        """Adding some scores to instance`s score."""
        if 0 <= score <= 10:
            next_level_score = min(i for i in SCORES if i > self.score)
            self.score += score
            if self.score >= next_level_score:
                self.level = SCORES[next_level_score]
            self.save()
        else:
            pass    # some mistake

    def get_avatar_url(self):
        if self.avatar is None:
            return settings.MEDIA_URL + "/uploads/avatars/default.png"
        return settings.MEDIA_URL + self.avatar.url

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
