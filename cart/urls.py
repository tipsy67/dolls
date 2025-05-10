from django.urls import path

from cart.apps import CartConfig
from cart.views import (OrderDetailView, OrderListView, buy_now, cart_add,
                        cart_detail, cart_partial_update, cart_remove,
                        cart_update, get_cart, order_create)

appname = CartConfig.name

urlpatterns = [
    path('cart/', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('buy_now/<int:product_id>/', buy_now, name='buy_now'),
    path('order-create/', order_create, name='order_create'),
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('order-detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('ajax/cart/get/', get_cart, name='get_cart'),
    path("ajax/cart/update/", cart_partial_update, name="cart_partial_update"),
]
