"""
Twitch OAuth2 backend, docs at:
    https://python-social-auth.readthedocs.io/en/latest/backends/goodgame.html
"""
from social_core.backends import oauth


class GoodGameOAuth2(oauth.BaseOAuth2):
    """GoodGame OAuth authentication backend"""
    name = 'goodgame'
    ID_KEY = 'user_id'
    AUTHORIZATION_URL = 'https://api2.goodgame.ru/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://api2.goodgame.ru/oauth'
    ACCESS_TOKEN_METHOD = 'POST'
    DEFAULT_SCOPE = ['channel.subscribers']
    REDIRECT_STATE = False

    def get_user_id(self, details, response):
        return response["user"].get(self.ID_KEY)

    def get_user_details(self, response):
        return {
            'username': response['user'].get('username'),
            #: no email directly could be fetched
            'first_name': '',
            'last_name': ''
        }

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json(
            'https://api2.goodgame.ru/info',
            params={'access_token': access_token}
        )
