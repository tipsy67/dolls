from django.core.paginator import Paginator
from django.shortcuts import render

from config.settings import PRODUCT_PER_PAGE
from dolls.models import Category, Product
from dolls.src.utils import get_random_reviews, get_queryset_from_cache
from tags.models import Tag
from tags.tag import CheckedTag
from tunes.models import Banner


def main_page(request):

    banner_list = Banner.objects.filter(is_published=True)

    category_list = Category.objects.filter(is_published=True)

    product_list = Product.objects.filter(is_published=True).order_by('?')

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

    tag_list = get_queryset_from_cache('tag_list')
    category_list = get_queryset_from_cache('category_list')
    sale_list = get_queryset_from_cache('sale_list')

    if cat is not None:
        product_list = Product.objects.filter(
            is_published=True, category_id=cat
        ).order_by('name')
    else:
        product_list = Product.objects.filter(is_published=True).order_by('name')

    tags = CheckedTag(request)
    if tags:
        product_list = product_list.filter(tags__pk__in=tags.tags)

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
        'tag_list': tag_list,
    }

    return render(request, 'dolls/shop.html', context)


def product_single_view(request, pk):
    product = Product.objects.filter(is_published=True, pk=pk).first()
    if product is not None:
        context = {
            'product': product,
        }
        return render(request, 'dolls/shop-single.html', context)

    return render(request, 'dolls/404.html')
