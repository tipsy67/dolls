from django.db.models.functions import Random

from django.core.paginator import Paginator
from django.shortcuts import render

from blog.models import BlogArticle
from config.settings import PRODUCT_PER_PAGE, BLOG_PER_PAGE
from dolls.models import Category, Product
from dolls.src.utils import get_random_reviews, get_queryset_from_cache
from tags.models import Tag
from tags.tag import CheckedTag, ProductCheckedTag
from tunes.models import Banner


def main_page(request):

    banner_list = Banner.objects.filter(is_published=True)
    category_list = get_queryset_from_cache('category_list_product')

    objects_list = []
    for category in category_list:
        product_list = Product.objects.filter(
            is_published=True, category=category
        ).order_by(Random())[:PRODUCT_PER_PAGE]
        objects_list.append(
            {'pk': category.pk, 'name': category.name, 'product_list': product_list}
        )

    blog_list = BlogArticle.objects.filter(is_published=True).order_by(Random())[
        :BLOG_PER_PAGE
    ]

    context = {
        'objects_list': objects_list,
        'blog_list': blog_list,
        'testimonial_list': get_random_reviews(request),
        'banner_list': banner_list,
        'home': 'active',
    }

    return render(request, 'dolls/index.html', context)


def product_list_view(request, cat=None):

    tag_list = get_queryset_from_cache('tag_list_product')

    category_list = get_queryset_from_cache('category_list_product')
    sale_list = get_queryset_from_cache('sale_list')

    if cat is not None:
        product_list = Product.objects.filter(
            is_published=True, category_id=cat
        ).order_by('name')
    else:
        product_list = Product.objects.filter(is_published=True).order_by('name')

    tags = ProductCheckedTag(request)
    if tags:
        product_list = product_list.filter(tags__pk__in=tags.tags)

    paginator = Paginator(product_list, PRODUCT_PER_PAGE)
    page_num_product = request.GET.get('page', 1)
    page_product = paginator.get_page(page_num_product)

    context = {
        'product_list': page_product,
        'category_list': category_list,
        'testimonials': get_random_reviews(request),
        'shop': 'active',
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


def product_preview_update(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if product is not None:
        context = {
            'product': product,
        }
        return render(request, 'popup-preview.html', context)

    return render(request, 'dolls/404.html')


def about(request):
    context = {}

    return render(request, 'dolls/about.html')


def history(request):
    context = {}

    return render(request, 'dolls/history.html')

def privacy_policy(request):
    context = {}

    return render(request, 'dolls/privacy-policy.html')

def shipping(request):
    context = {}

    return render(request, 'dolls/shipping.html')

def user_agreement(request):
    context = {}

    return render(request, 'dolls/user-agreement.html')

def contact_us(request):
    context = {}

    return render(request, 'dolls/contact-us.html')