from django.urls import path

from tags.apps import TagsConfig
from tags.views import change_tag, clear_tag

app_name = TagsConfig.name

urlpatterns = [
    path('change-tag/<int:tag_pk>/', change_tag, name='change_tag'),
    path('clear-tag/', clear_tag, name='clear_tag'),
]
