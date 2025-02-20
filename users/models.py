import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    tg_chat_id = models.CharField(
        max_length=50, **NULLABLE, verbose_name="телеграм chat id"
    )
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='аватар')
    phone = models.CharField(max_length=30, verbose_name='телефон')
    token = models.CharField(max_length=100, **NULLABLE, verbose_name='токен')

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.last_name} {self.first_name[:1]}."

    @property
    def fio(self):
        return f'{self.last_name} {self.first_name}'

    @staticmethod
    def generate_password(length: int):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))

        return password
