import json

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render

from subscribes.models import Recipients


@login_required
def subscribe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            new_subscribe = Recipients(email=email, author=request.user)
            new_subscribe.save()
            response = {'success': True}
        except Exception as e:
            response = {'success': False}

    return JsonResponse(response)


@login_required
def unsubscribe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            new_subscribe = Recipients.objects.filter(email=email).first()
            new_subscribe.delete()
            response = {'success': True}
        except Exception as e:
            response = {'success': False}

    return JsonResponse(response)


@login_required
def unsubscribe_page(request):
    context = {}

    return render(request, 'dolls/unsubscribe.html', context)
