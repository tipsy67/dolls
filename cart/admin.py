from django.contrib import admin

from cart.models import Order, OrderItem
from django.urls import reverse
from django.utils.html import format_html

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
    list_filter = ('user' ,'status')
    search_fields = ('user__last_name',)

    def total_cost(self, obj):
        return obj.get_total_cost()

    @admin.display(description='поставщик')
    def user_link(self, instance):
        if instance.user is not None:
            url = reverse('admin:users_user_change', args=[instance.user.pk])
            return format_html('<a href="{}">{}</a>', url, instance.user)
        return "нет поставщика"