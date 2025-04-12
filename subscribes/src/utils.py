from config.settings import CACHE_ENABLED
from django.core.cache import cache

from subscribes.models import Recipients


def get_list_from_base() -> list:
    obj = Recipients.objects.values_list('email', flat=True)

    return obj


def get_recipients():
    if CACHE_ENABLED:
        cache_data = cache.get('email')
        if cache_data is None:
            cache_data = get_list_from_base()
            cache.set('email', cache_data)

        return cache_data

    return get_list_from_base()