from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse
from config.settings import LOGIN_URL
from dolls.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib import messages


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if product:
        if request.method == 'POST':
            form = CartAddProductForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                quantity = cd.get('quantity', 1)
                override_quantity = cd.get('override', False)
                cart.add(product=product, quantity = quantity, override_quantity = override_quantity)
        else:
            quantity = 1
            cart.add(product=product, quantity=quantity, )
        messages.success(request, f"Вы добавили в корзину {product.name} - {quantity} шт.")
    else:
        messages.error(request, "при добавлении в корзину произошла ошибка")
    url = request.META.get('HTTP_REFERER') #+ "#product_" + str(product_id)
    return redirect(url)


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return render(request, 'dolls/cart.html', {'cart': cart})

# @require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')