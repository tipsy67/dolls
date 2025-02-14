from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import F, Q
from config.settings import PRODUCT_PER_PAGE
from dolls.models import Category, Product
from dolls.src.utils import get_random_reviews
from tunes.models import Banner


def main_page(request):

    banner_list = Banner.objects.filter(is_published=True)

    category_list = Category.objects.filter(is_published=True)

    product_list = Product.objects.filter(is_published=True).order_by(
            '?'
        )


    # blog_set = Blog.objects.filter(is_published=True).order_by('?')
    # blog_list = blog_set[:3]

    context = {
        'product_list': product_list,
        'category_list': category_list,
        # 'blog_list': blog_list,
        'testimonial_list': get_random_reviews(request),
        'banner_list': banner_list,
        'home': 'active',
    }


    return render(request, 'dolls/index.html', context)

def product_list_view(request, cat=None):

    category_list = Category.objects.filter(is_published=True)

    if cat is not None:
        product_list = Product.objects.filter(is_published=True, category_id=cat).order_by('name')
    else:
        product_list = Product.objects.filter(is_published=True).order_by('name')

    sale_list = Product.objects.filter(~Q(old_price=0) & ~Q(old_price=F('price')), is_published=True).order_by('-update_at')[:3]

    paginator = Paginator(product_list, PRODUCT_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'product_list': page_obj,
        'category_list': category_list,
        'testimonials': get_random_reviews(request),
        'shop': 'active',
        'page_number': page_number,
        'category_pk': cat,
        'sale_list': sale_list,
    }

    return render(request, 'dolls/shop.html', context)