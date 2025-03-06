from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse
from config.settings import LOGIN_URL
from dolls.models import Product
from users.models import User
from .cart import Cart

from django.contrib import messages

from .forms import OrderCreateForm
from .models import OrderItem


def cart_update(request):
    cart = Cart(request)
    for key, value in cart.cart.items():
        quantity_in_cart = request.GET.get(f'quantity{key}', 1)
        product = value.get('product', None)

    url = request.META.get('HTTP_REFERER')  # + "#product_" + str(product_id)
    return redirect(url)


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if product:
        if request.method == 'POST':
            quantity = request.POST.get(f'quantity', 1)
            cart.add(product=product, quantity=quantity, override_quantity=True)
        else:
            quantity = 1
            cart.add(
                product=product,
                quantity=quantity,
            )
        messages.success(
            request, f"Вы добавили в корзину {product.name} - {quantity} шт."
        )
    else:
        messages.error(request, "при добавлении в корзину произошла ошибка")
    url = request.META.get('HTTP_REFERER')  # + "#product_" + str(product_id)
    return redirect(url)


def cart_detail(request):
    cart = Cart(request)
    if request.method == 'POST':
        for item in cart:
            product = item.get('product')
            if product:
                item['quantity'] = min(
                    int(request.POST.get(f'quantity{product.pk}', 1)), product.quantity
                )

    return render(
        request,
        'dolls/cart.html',
        {'cart': cart, 'return_url': request.META.get('HTTP_REFERER')},
    )


# @require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            return render(request,
                          'dolls/order-created.html',
                          {'order': order})
    else:
        user = User.objects.filter(pk=request.user.pk).first()
        dict_ = vars(user)
        address = vars (user.addresses.filter(is_active=True).first())
        if address: dict_ = dict_ | address
        form = OrderCreateForm(dict_)

    context = {
        'title_form': "Создание заказа",
        'form' :form,
    }

    return render(
        request,
        'dolls/order-form.html',
        context,
    )
