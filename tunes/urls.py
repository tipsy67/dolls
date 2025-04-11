from django.urls import path
from tunes.apps import TunesConfig
from tunes.views import subscribe

appname = TunesConfig.name

urlpatterns = [
    path("ajax/subscribe/", subscribe, name="subscribe"),
]