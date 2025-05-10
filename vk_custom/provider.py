from allauth.socialaccount.providers.vk.provider import VKProvider

from vk_custom.views import VKCustomOAuth2Adapter


class CustomVKProvider(VKProvider):
    id = 'vk_custom'
    name = 'VK (custom)'
    adapter_class = VKCustomOAuth2Adapter
    oauth2_adapter_class = VKCustomOAuth2Adapter

    def get_auth_params(self):
        params = super().get_auth_params()
        params['code_challenge'] = self.get_pkce_params()  # Добавляем PKCE
        params['code_challenge_method'] = 'S256'
        return params


# providers.registry.register(CustomVKProvider)
provider_classes = [CustomVKProvider]
