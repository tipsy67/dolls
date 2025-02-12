from config.settings import NUMBER_OF_REVIEWS_DISPLAYED
from tunes.models import Feedback


def get_random_reviews(request):
    reviews_set = request.session.get('reviews')
    if reviews_set is None:
        reviews_set = Feedback.objects.filter(is_published=True).order_by('?')
        request.session['reviews'] = reviews_set

    return reviews_set[:NUMBER_OF_REVIEWS_DISPLAYED]



