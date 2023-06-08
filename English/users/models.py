from django.core.files import File
from django.db import models
from django.contrib.auth.models import AbstractUser
from passlib.hash import django_pbkdf2_sha256


def load_default_avatar():
    return File(AVATARS_DIR + "/default_avatar.png")


AVATARS_DIR = "media/avatars/"


class User(AbstractUser):
    location = models.CharField("Location", max_length=200)
    avatar = models.ImageField("Avatar", upload_to=AVATARS_DIR, default=load_default_avatar)
    level = models.CharField("Уровень английского", max_length=100, default='A1', blank=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ("email", 'password', 'location')

    @classmethod
    def register(cls, **data):
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
        user = cls.objects.get(username=username)
        if django_pbkdf2_sha256.verify(password, user.password):
            return user

        return None

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
