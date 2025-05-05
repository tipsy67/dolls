from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView
from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter


class VKCustomOAuth2Adapter(VKOAuth2Adapter):
    provider_id = 'vk_custom'

    access_token_url = "https://oauth.vk.com/access_token"  # nosec
    authorize_url = "https://id.vk.com/authorize"

    supports_state = True

oauth2_login = OAuth2LoginView.adapter_view(VKCustomOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(VKCustomOAuth2Adapter)
