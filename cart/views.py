import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from config.settings import CART_SESSION_ID, LOGIN_URL
from dolls.models import Product
from dolls.tasks import sendmail
from tunes.src.utils import get_value_from_tunes
from users.models import User

from .cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem


def cart_update(request):
    cart = Cart(request)
    for key, value in cart.cart.items():
        quantity_in_cart = request.GET.get(f'quantity{key}', 1)
        product = value.get('product', None)

    url = request.META.get('HTTP_REFERER')  # + "#product_" + str(product_id)
    return redirect(url)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # data = json.loads(request.body)
    # quantity = int(data.get('quantity', 1))
    quantity = 1

    if product and product.quantity > 0:
        # Add product to cart
        cart.add(product=product, quantity=quantity, override_quantity=False)

        response_data = {
            'success': True,
            'message': f"Вы добавили в корзину {product.name} - {quantity} шт.",
            'cart_total': len(cart),
            'product_name': product.name,
            'quantity': quantity,
        }
    else:
        response_data = {
            'success': False,
            'message': "При добавлении в корзину произошла ошибка",
        }

    if request.headers.get('Content-Type') == 'application/json':
        return JsonResponse(response_data)

    if response_data['success']:
        messages.success(request, response_data['message'])
    else:
        messages.error(request, response_data['message'])

    url = request.META.get('HTTP_REFERER', '/')
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
                if item['quantity'] == 0:
                    cart.remove(product)
        cart.save()
    context = {
        'cart': cart,
        'return_url': request.META.get('HTTP_REFERER'),
    }

    return render(
        request,
        'dolls/cart.html',
        context,
    )


def buy_now(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = 1

    if product and product.quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=False)

    return redirect('cart:order_create')


# @require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    try:
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return JsonResponse({'success': True})
    # return redirect('cart:cart_detail')
    except:
        return JsonResponse({'success': False})


def cart_partial_update(request):
    return render(request, "popup-cart.html")


def get_cart(request):
    cart = Cart(request)
    response = {'success': True, 'cart_length': len(cart)}
    return JsonResponse(response)


@login_required
def order_create(request):
    cart = Cart(request)
    if not cart:
        return render(request, 'dolls/404.html')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )

            cart.clear()
            context = {
                'obj': order,
            }
            sendmail.delay(
                [order.email, get_value_from_tunes('author_email')],
                f"Заказ создан",
                render_to_string('cart/order-created.html', context),
            )

            return render(request, 'dolls/order-created.html', {'order': order})
    else:
        user = User.objects.filter(pk=request.user.pk).first()
        dict_ = vars(user)
        address_obj = user.addresses.filter(is_active=True).first()
        if address_obj:
            dict_ |= vars(address_obj)
        form = OrderCreateForm(dict_)

    context = {
        'title_form': "Создание заказа",
        'form': form,
    }

    return render(
        request,
        'dolls/order-form.html',
        context,
    )


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'dolls/order-detail.html'
    extra_context = {
        'title_form': "Вы действительно хотите удалить этот адрес?",
        # 'back_url': reverse_lazy(request.GET.get('next', '/'))
    }


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'order_list'
    template_name = 'dolls/order-list.html'
    extra_context = {
        'title_form': "Вы действительно хотите удалить этот адрес?",
        # 'back_url': reverse_lazy(request.GET.get('next', '/'))
    }
