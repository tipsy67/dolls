from django.core.paginator import Paginator
from django.shortcuts import render

from blog.models import BlogArticle
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
    blog_list = BlogArticle.objects.filter(is_published=True).order_by('?')


    paginator_product = Paginator(product_list, PRODUCT_PER_PAGE)
    page_num_product = request.GET.get('page_prod', 1)
    page_product = paginator_product.get_page(page_num_product)

    paginator_blog = Paginator(blog_list, 3)
    page_num_blog = request.GET.get('page_blog', 1)
    page_blog = paginator_blog.get_page(page_num_blog)

    context = {
        'product_list': page_product,
        'category_list': category_list,
        'blog_list': page_blog,
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
