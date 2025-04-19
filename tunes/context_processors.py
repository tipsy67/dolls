from tunes.src.utils import get_value_from_tunes


def get_tunes(request):
    context = {}
    context['author_phone'] = get_value_from_tunes('author_phone')
    context['author_email'] = get_value_from_tunes('author_email')
    context['limit_free_shipping'] = get_value_from_tunes('limit_free_shipping')
    context['insta_name'] = get_value_from_tunes('insta_name')

    return context
