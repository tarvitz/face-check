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
    #: TODO await when GG provide email user retrieve through scope
    #: https://goodgame.ru/topic/67865#comment427
    DEFAULT_SCOPE = ['channel.subscribers']
    REDIRECT_STATE = False

    def get_user_id(self, details, response):
        return response["user"].get(self.ID_KEY)

    def get_user_details(self, response):
        return {
            'username': response['user'].get('username'),
            #: currently there's no email
            'email': response['user'].get('email'),
            'first_name': '',
            'last_name': ''
        }

    def user_data(self, access_token, *args, **kwargs):
        #: treat this as hacky as far as simple info does not return
        #: email address, but we can retrieve it from another endpoint
        return self.get_json(
            'https://api2.goodgame.ru/info',
            params={'access_token': access_token}
        )
