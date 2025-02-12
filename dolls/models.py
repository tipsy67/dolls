from config.settings import NULLABLE
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_published = models.BooleanField(default=False, verbose_name='Активно')
    active_on_main_page = models.BooleanField(
        default=False, verbose_name='Активно на гл.стр.'
    )

    ordering = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория',
    )
    parameter = models.CharField(max_length=30, verbose_name='Параметр', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='Активно')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    name = models.CharField( max_length=50, unique=True , verbose_name='Имя')
    image = models.ImageField(upload_to='upload/product_images' , verbose_name='Фото')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='images', verbose_name='Продукт')
    is_published = models.BooleanField(default=False, verbose_name='Активно')
    active_on_main_page = models.BooleanField(
        default=False, verbose_name='Активно на гл.стр.'
    )


    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"
