from django.urls import path

from tags.apps import TagsConfig
from tags.views import change_tag

app_name = TagsConfig.name

urlpatterns = [
    path('change-tag/<int:tag_pk>/', change_tag, name='change_tag'),
]
