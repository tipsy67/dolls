from django.urls import path
from cart.apps import CartConfig
from cart.views import cart_add, cart_detail, cart_remove, cart_update, order_create

appname = CartConfig.name

urlpatterns = [
    path('cart/', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),

    path('order/', order_create, name='order_create'),

]
