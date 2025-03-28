from django.core.cache import cache

from config.settings import CACHE_ENABLED
from tunes.models import TunesDict


def get_value_from_base(key):
    obj = TunesDict.objects.filter(key=key).first()
    return obj.value

def get_value_from_tunes(key):
    if CACHE_ENABLED:
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = get_value_from_base(key)
            cache.set(key, cache_data)

        return cache_data

    return get_value_from_base(key)