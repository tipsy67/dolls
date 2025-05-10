from django.apps import AppConfig


class VkCustomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vk_custom"

    def ready(self):
        from allauth.socialaccount.providers import registry

        from vk_custom.provider import CustomVKProvider

        registry.register(CustomVKProvider)
