from django.db import models

class Recipients(models.Model):
    email = models.EmailField(unique=True, verbose_name='Почта')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    author = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Автор')


    class Meta:
        ordering = ['email']
        verbose_name = 'адрес для рассылок'
        verbose_name_plural = 'адреса для рассылок'

    def __str__(self):
        return f"{self.email}"


class Article(models.Model):
    is_test = models.BooleanField(default=True, verbose_name='Тест')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменена')

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'