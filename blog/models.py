from django.db import models
from django.template.defaultfilters import truncatechars
from pytils.translit import slugify

from config.settings import AUTH_USER_MODEL
from dolls.models import Category
from users.models import NULLABLE, User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    article = models.ForeignKey(
        'BlogArticle',
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Статья",
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родитель",
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Владелец",
    )
    text = models.CharField(max_length=1000, verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    class MPTTMeta:
        order_insertion_by = ['created_at']

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"{self.owner}: {self.text[:20]}"


class BlogArticle(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, unique=True, verbose_name='Slug')
    image = models.ImageField(upload_to='blog/', blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')
    views_counter = models.IntegerField(default=0, verbose_name='Количество просмотров')
    content = models.TextField(verbose_name='Содержимое')
    owner = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name='blogs',
        verbose_name='Владелец',
    )
    users_like = models.ManyToManyField(
        AUTH_USER_MODEL, related_name='images_liked', blank=True
    )
    tags = models.ManyToManyField(
        'tags.Tag', blank=True, related_name='tags_article', verbose_name="Теги"
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name='articles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title}'

    @property
    def short_content(self):
        return truncatechars(self.content, 100)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super(BlogArticle, self).save(*args, **kwargs)
