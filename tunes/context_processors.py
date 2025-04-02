from tunes.models import Contact
from tunes.src.utils import get_value_from_tunes


def get_contact(request):
    return {'contact': Contact.objects.filter(is_published=True).first()}


def get_limit_free_shipping(request):
    return {'limit_free_shipping': get_value_from_tunes('limit_free_shipping')}
