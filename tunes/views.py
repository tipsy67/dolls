import json

from django.http.response import JsonResponse

from tunes.models import Subscriber


def subscribe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            new_subscribe = Subscriber(email=email, author=request.user)
            new_subscribe.save()
            response = {'success': True}
        except Exception as e:
            response = {'success': False}

    return JsonResponse(response)
