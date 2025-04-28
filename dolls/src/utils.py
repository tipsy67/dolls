from config.settings import NUMBER_OF_REVIEWS_DISPLAYED, CACHE_ENABLED
from dolls.models import Category, Product
from tags.models import Tag
from tunes.models import Feedback
from django.core.cache import cache
from django.db.models import F, Q
from django.db.models.functions import Random


def get_random_reviews(request):
    reviews_set = request.session.get('reviews')
    if reviews_set is None:
        reviews_set = Feedback.objects.filter(is_published=True).order_by(Random())
        request.session['reviews'] = reviews_set

    return reviews_set[:NUMBER_OF_REVIEWS_DISPLAYED]


def get_model_queryset(list_name: str):
    if list_name == 'tag_list_product':
        queryset= None
        # queryset = Tag.objects.filter(tags_product__isnull=False).distinct()
    elif list_name == 'tag_list_article':
        queryset= None
        # queryset = Tag.objects.filter(tags_article__isnull=False).distinct()
    elif list_name == 'category_list_product':
        queryset = Category.objects.filter(
            is_published=True, products__isnull=False
        ).distinct()
    elif list_name == 'category_list_blog':
        queryset = Category.objects.filter(
            is_published=True, article__isnull=False
        ).distinct()
    elif list_name == 'sale_list':
        queryset = Product.objects.filter(
            ~Q(old_price=0) & ~Q(old_price=F('price')), is_published=True
        ).order_by('-update_at')[:3]

    return queryset


def get_queryset_from_cache(list_name: str):
    if CACHE_ENABLED:
        cache_data = None  # cache.get(list_name)
        if cache_data is None:
            cache_data = get_model_queryset(list_name)
            cache.set(list_name, cache_data)

        return cache_data

    return get_model_queryset(list_name)
