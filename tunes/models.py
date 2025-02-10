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


class Quote(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    quote = models.TextField(blank=True, verbose_name='Цитата')
    is_published = models.BooleanField(default=False, verbose_name='Публиковать')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        # db_table = 'optics_quote'
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'


class Contact(models.Model):
    country = models.CharField(max_length=50, verbose_name='Страна')
    inn = models.CharField(max_length=20, verbose_name='ИНН')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Эл.почта')
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name='Активно')


    def __str__(self):
        return f"{self.email}"

    class Meta:
        # db_table = 'optics_contact'
        ordering = ['-updated_at']
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class TunesDict(models.Model):
    key = models.CharField(max_length=30, unique=True, verbose_name='Ключ')
    value_int = models.CharField(**NULLABLE, verbose_name='Целочисленное значение')
    value_char = models.CharField(max_length=100, **NULLABLE,  verbose_name='Строковое значение')
    value_time = models.TimeField( **NULLABLE,  verbose_name='Константа времени')
    value_date = models.DateField( **NULLABLE,  verbose_name='Константа даты')

    class Meta:
        ordering = ['key']
        verbose_name = 'Тонкие настройки'
        verbose_name_plural = 'Тонкие настройки'

    def __str__(self):
        return f"{self.key}"


class Banner(models.Model):
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    content = models.TextField(**NULLABLE, verbose_name='Описание')
    image = models.ImageField(
        upload_to='tunes/', **NULLABLE, verbose_name='Изображение'
    )
    is_published = models.BooleanField(default=False, verbose_name='Активно')

    class Meta:
        ordering = ['title']
        verbose_name = 'Заглавный баннер'
        verbose_name_plural = 'Заглавные баннеры'

    def __str__(self):
        return f"{self.title}"

    @property
    def short_content(self):
        return f"{self.content[:40]} ..."