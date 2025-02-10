from tunes.models import Contact

def get_contact(request):
    return {'contact': Contact.objects.filter(is_published=True).first()}