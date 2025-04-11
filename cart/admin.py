from django.contrib import admin
from django.template.loader import render_to_string

from cart.models import Order, OrderItem
from django.urls import reverse
from django.utils.html import format_html
from dolls.tasks import sendmail

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user_link',
        'status',
    )
    inlines = (OrderItemInline,)
    readonly_fields = ('total_cost',)
    list_filter = ('user', 'status')
    search_fields = ('user__last_name',)

    def total_cost(self, obj):
        return obj.get_total_cost()

    @admin.display(description='поставщик')
    def user_link(self, instance):
        if instance.user is not None:
            url = reverse('admin:users_user_change', args=[instance.user.pk])
            return format_html('<a href="{}">{}</a>', url, instance.user)
        return "нет поставщика"

    def save_model(self, request, obj, form, change):
        if "status" in form.changed_data:
            context ={
                'obj': obj,
            }

            sendmail.delay(
                [obj.email],
                f"Статус заказа",
                render_to_string('cart/order-status.html', context),
            )
        super().save_model(request, obj, form, change)