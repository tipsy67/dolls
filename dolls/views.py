from django.shortcuts import render

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
    }


    return render(request, 'dolls/index.html', context)
