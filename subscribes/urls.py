from django.urls import path

from subscribes.apps import SubscribesConfig
from subscribes.views import subscribe, unsubscribe, unsubscribe_page

appname = SubscribesConfig.name

urlpatterns = [
    path("ajax/subscribe/", subscribe, name="subscribe"),
    path("ajax/unsubscribe/", unsubscribe, name="unsubscribe"),
    path("unsubscribe-page/", unsubscribe_page, name="unsubscribe_page"),
]
