from django.core.files import File
from django.db import models
from django.contrib.auth.models import AbstractUser
from passlib.hash import django_pbkdf2_sha256
import logging


logger = logging.getLogger(__name__)
AVATARS_DIR = "media/avatars/"

SCORES = {
    1000: "A1",
    2000: "A2",
    3000: "B1",
    4000: "B2",
    5000: "C1",
    6000: "C2"
}


def load_default_avatar():
    logger.debug(str(File(AVATARS_DIR + "/default_avatar.png")))
    return File(AVATARS_DIR + "/default_avatar.png")


class User(AbstractUser):

    class Levels(models.TextChoices):
        A1 = ("A1", "(А1) – начальный")
        A2 = ("A2", "(А2) – ниже среднего")
        B1 = ("B1", "(В1) – средний")
        B2 = ("B2", "(В2) – выше среднего")
        C1 = ("C1", "(C1) – продвинутый")
        C2 = ("C2", "(C2) – профессиональный уровень владения")

    location = models.CharField("Location", max_length=200)
    avatar = models.ImageField("Avatar", upload_to=AVATARS_DIR, default=load_default_avatar)
    level = models.CharField("Уровень английского", max_length=100, default='A1', blank=True)
    score = models.IntegerField("Очки английского", null=True, default=0, blank=True)
    # need_exam = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ("email", 'password', 'location')

    @classmethod
    def register(cls, **data):
        """Create instance and hash password"""
        psw = data.get('password')
        if psw is not None:
            hash_psw = django_pbkdf2_sha256.hash(psw)
            data.update(password=hash_psw)
            user = cls.objects.create(**data)
            user.save()
            return user

        return None

    @classmethod
    def login(cls, username: str, password: str):
        """Verify user password hash"""
        user = cls.objects.get(username=username)
        if django_pbkdf2_sha256.verify(password, user.password):
            return user

        return None

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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


