from django.db import models

from config.settings import NULLABLE


class Feedback(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    message = models.TextField(blank=True, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    is_published = models.BooleanField(default=False, verbose_name='Публиковать')

    def __str__(self):
        return f"{self.name}, {self.created_at}"

    class Meta:
        # db_table = 'optics_feedback'
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class TunesDict(models.Model):
    key = models.CharField(max_length=30, unique=True, verbose_name='Ключ')
    value = models.CharField(
        max_length=100, **NULLABLE, verbose_name='Строковое значение'
    )
    description = models.CharField(max_length=100, **NULLABLE, verbose_name='Описание')

    class Meta:
        ordering = ['key']
        verbose_name = 'Тонкие настройки'
        verbose_name_plural = 'Тонкие настройки'

    def __str__(self):
        return f"{self.key}"


class Banner(models.Model):
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    image = models.ImageField(
        upload_to='tunes/', **NULLABLE, verbose_name='Изображение'
    )
    is_published = models.BooleanField(default=False, verbose_name='Активно')

    class Meta:
        ordering = ['title']
        verbose_name = 'Инстаграм'
        verbose_name_plural = 'Инстаграм'

    def __str__(self):
        return f"{self.title}"
