from allauth.socialaccount.providers.oauth2.views import (
    OAuth2CallbackView,
    OAuth2LoginView,
)
from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter


class VKCustomOAuth2Adapter(VKOAuth2Adapter):
    provider_id = 'vk_custom'

    access_token_url = "https://oauth.vk.com/access_token"  # nosec
    authorize_url = "https://id.vk.com/authorize"

    supports_state = True

    def complete_login(self, request, app, token, **kwargs):
        """
        Полная реализация авторизации VK ID по схеме code_v2:
        1. Проверка state из сессии
        2. Обмен code + code_verifier + device_id на токены
        3. Получение данных пользователя
        4. Создание социального аккаунта
        """
        from allauth.socialaccount.adapter import get_adapter
        from django.core.exceptions import SuspiciousOperation
        from requests.exceptions import RequestException

        # 1. Проверка state (должен быть в сессии)
        session_state = request.session.pop('vk_auth_state', None)
        callback_state = request.GET.get('state')
        if not session_state or session_state != callback_state:
            raise SuspiciousOperation("Invalid VK state parameter")

        # 2. Получаем обязательные параметры из callback
        auth_code = request.GET.get('code')
        device_id = request.GET.get('device_id')
        code_verifier = request.session.pop('vk_code_verifier', None)

        if not all([auth_code, device_id, code_verifier]):
            raise ValueError(
                "Missing required auth parameters (code, device_id or code_verifier)"
            )

        try:
            session = get_adapter().get_requests_session()

            # 3. Обмен кода на токены через новый endpoint
            token_response = session.post(
                "https://id.vk.com/oauth2/auth",
                data={
                    "grant_type": "authorization_code",
                    "client_id": app.client_id,
                    "client_secret": app.secret,
                    "redirect_uri": self.get_callback_url(request),
                    "code": auth_code,
                    "code_verifier": code_verifier,
                    "device_id": device_id,
                    # "v": "5.199"
                },
                # timeout=10
            ).json()

            if 'error' in token_response:
                error_msg = token_response.get(
                    'error_description', 'VK token exchange failed'
                )
                raise RequestException(f"VK Token Error: {error_msg}")

            # 4. Получаем данные пользователя
            user_data = session.get(
                "https://api.vk.com/method/users.get",
                params={
                    "access_token": token_response['access_token'],
                    # "v": "5.199",
                    "fields": "first_name,last_name,photo_max_orig,email,screen_name",
                    "lang": "ru",
                },
            ).json()

            if 'error' in user_data:
                raise RequestException(
                    f"VK API Error: {user_data['error']['error_msg']}"
                )

            # 5. Формируем данные для социального аккаунта
            extra_data = {
                **user_data.get('response', [{}])[0],
                "device_id": device_id,
                "access_token": token_response['access_token'],
                "refresh_token": token_response.get('refresh_token'),
                "id_token": token_response.get('id_token'),
                "token_expires_in": token_response.get('expires_in'),
            }

            # 6. Добавляем email, если он пришел в токен-ответе
            if 'email' not in extra_data and token_response.get('email'):
                extra_data['email'] = token_response['email']

            return self.get_provider().sociallogin_from_response(request, extra_data)

        except RequestException as e:
            error_context = {
                "error": str(e),
                "auth_code": auth_code,
                "device_id": device_id,
                # "api_version": "5.199"
            }
            raise Exception(f"VK Auth Failed: {error_context}")


oauth2_login = OAuth2LoginView.adapter_view(VKCustomOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(VKCustomOAuth2Adapter)
