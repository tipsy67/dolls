from django.db import models

from config.settings import NULLABLE
from dolls.models import Product


class Order(models.Model):
    STATUS_ORDER = {
        'CREATED': "Создан",
        'NONPAID': "К оплате",
        'PAID': "Оплачен",
        'SEND': "Отправлен",
        'SHIPPED': "Доставлен",
    }
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Эл.почта')
    country = models.CharField(max_length=50, verbose_name='Страна')
    postal_code = models.CharField(max_length=20, verbose_name='Индекс')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    comment = models.CharField(max_length=255, verbose_name='Комментарий', **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to='users.User', on_delete=models.CASCADE, related_name='orders'
    )
    status = models.CharField(max_length=10, choices=STATUS_ORDER, default='CREATED')

    class Meta:
        # db_table = 'optics_contact'
        ordering = ['-created_at']
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_status(self):
        return self.STATUS_ORDER[self.status]

    def get_address(self):
        return f"{self.postal_code}, {self.country}, {self.address}"

    def get_recipient(self):
        str_ = f"{self.last_name} {self.first_name[:1]}."
        if self.middle_name:
            str_ = str_ + f"{self.middle_name[:1]}."
        return str_


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
