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


class Address(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    country = models.CharField(max_length=50, verbose_name='Страна')
    zip = models.CharField(max_length=20, verbose_name='Индекс')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    comment = models.CharField(max_length=255, verbose_name='Комментарий', **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, verbose_name='Активно')
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='addresses')


    def __str__(self):
        return f"{self.name}"

    class Meta:
        # db_table = 'optics_contact'
        ordering = ['-updated_at']
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'