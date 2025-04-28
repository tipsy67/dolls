from config.settings import NULLABLE
from django.db import models
from django.urls import reverse
from django.db.models.functions import Random


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_published = models.BooleanField(default=False, verbose_name='Активно')
    active_on_main_page = models.BooleanField(
        default=False, verbose_name='Активно на гл.стр.'
    )

    ordering = ['name']

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    short_description = models.TextField(**NULLABLE, verbose_name='Краткое описание')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    quantity = models.PositiveSmallIntegerField(**NULLABLE, verbose_name='Количество')
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Цена')
    old_price = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name='Старая цена'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    tags = models.ManyToManyField(
        'tags.Tag', blank=True, related_name='tags_product', verbose_name="Теги"
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория',
    )
    parameter = models.CharField(max_length=30, verbose_name='Параметр', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='Активно')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

    @property
    def one_image(self):
        return self.images.prefetch_related().all().order_by(Random()).first()

    @property
    def sale(self):
        return self.old_price != 0 and self.old_price != self.price


class Image(models.Model):
    name = models.CharField(max_length=50, **NULLABLE, verbose_name='Имя')
    image = models.ImageField(upload_to='upload/product_images', verbose_name='Фото')
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Продукт',
    )
    is_published = models.BooleanField(default=False, verbose_name='Активно')
    active_on_main_page = models.BooleanField(
        default=False, verbose_name='Активно на гл.стр.'
    )

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"
