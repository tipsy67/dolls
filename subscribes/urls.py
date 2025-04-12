from django.urls import path

from subscribes.apps import SubscribesConfig
from subscribes.views import subscribe, unsubscribe

appname = SubscribesConfig.name

urlpatterns = [
    path("ajax/subscribe/", subscribe, name="subscribe"),
    path("/unsubscribe/", unsubscribe, name="unsubscribe"),
]
