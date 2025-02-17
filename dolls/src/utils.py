from config.settings import NUMBER_OF_REVIEWS_DISPLAYED, CACHE_ENABLED
from dolls.models import Category, Product
from tags.models import Tag
from tunes.models import Feedback
from django.core.cache import cache
from django.db.models import F, Q

def get_random_reviews(request):
    reviews_set = request.session.get('reviews')
    if reviews_set is None:
        reviews_set = Feedback.objects.filter(is_published=True).order_by('?')
        request.session['reviews'] = reviews_set

    return reviews_set[:NUMBER_OF_REVIEWS_DISPLAYED]

def get_model_queryset(list_name:str):
    if list_name == 'tag_list':
        queryset = Tag.objects.all()
    elif list_name == 'category_list':
        queryset = Category.objects.filter(is_published=True)
    elif list_name == 'sale_list':
        queryset = Product.objects.filter(~Q(old_price=0) & ~Q(old_price=F('price')), is_published=True).order_by('-update_at')[:3]

    return queryset

def get_queryset_from_cache(list_name:str):
    if CACHE_ENABLED:
        cache_data = cache.get(list_name)
        if cache_data is None:
            cache_data = get_model_queryset(list_name)
            cache.set(list_name, cache_data)

        return cache_data

    return get_model_queryset(list_name)
