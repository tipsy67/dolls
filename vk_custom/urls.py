from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from vk_custom.apps import VkCustomConfig
from vk_custom.provider import CustomVKProvider

appname = VkCustomConfig.name

urlpatterns = default_urlpatterns(CustomVKProvider)
