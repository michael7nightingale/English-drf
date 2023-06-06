from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


def load_default_avatar():
    with open(settings.BASE_DIR + "/" + AVATARS_DIR + "/default_avatar.png", mode='rb') as image_file:
        return image_file.read()


AVATARS_DIR = "media/avatars/"


class User(AbstractUser):
    location = models.CharField("Location", max_length=200)

    def get_account(self):
        return Account.objects.get(user=self)


class Account(models.Model):
    avatar = models.ImageField("Avatar", upload_to=AVATARS_DIR, default=load_default_avatar)
    user = models.OneToOneField(to="User", on_delete=models.CASCADE)

