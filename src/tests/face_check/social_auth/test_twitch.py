"""
This module test Twitch Auth with injections provided in projects
Basic goal to verify working settings.SOCIAL_AUTH_PIPELINE with
projects modifications.

.. note::

    Some of functionality has been tested over mocking real working api
    responses, it means changing this module requires much work and it's
    not counted as e2e test cases are desired.
"""
from unittest import mock

from django.urls import reverse
from django.test import TestCase
from social_core.backends.oauth import OAuthAuth, BaseOAuth2
from social_core.backends.twitch import TwitchOAuth2

from face_check.consts import HttpStatus


class step(object):
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise exc_val


class TwitchLoginTest(TestCase):
    """
    whole pipeline:
    user -> twitch {auth} (complete) -> backend -> twitch {token} -> finish
    tested part started from complete push from twitch, emulated with mocks
    """
    @classmethod
    def setUpClass(cls):
        cls.auth_url_complete = reverse("social:complete", args=("twitch", ))
        super().setUpClass()

    def setUp(self):
        #: google oauth response to /complete/twitch/
        self.oauth_response = {
            'code': 'ih2o4ibvirjxipejc19cevcp6b0939',
            'scope': 'user_read',
            'state': 'FakeState'
        }
        self.auth_response = {
            'access_token': '1e84e29qi5u2gozvoqaoebauwnd90n',
            'expires_in': 13048,
            'refresh_token': 'wrrjc22jp1gjm1irld1iklvaaaq1j77pemhgsi8pye6x1hlrdy',
            'scope': ['user_read'],
            'token_type': 'bearer'
        }
        self.user_data = {
            'display_name': 'NickolasFox',
            '_id': 74767317,
            'name': 'nickolasfox',
            'type': 'user',
            'bio': 'Teh pirate',
            'created_at': '2014-11-08T19:58:27Z',
            'updated_at': '2018-12-15T20:11:41Z',
            'logo': 'https://static-cdn.jtvnw.net/jtv_user_pictures/'
                    'nickolasfox-profile_image-a6a3363661a933f9-300x300.png',
            '_links': {'self': 'https://api.twitch.tv/kraken/users/nickolasfox'},
            'email': 'tarvitz@blacklibrary.ru',
            'partnered': False,
            'notifications': {'push': True, 'email': True}
        }

    @mock.patch.object(OAuthAuth, 'validate_state')
    @mock.patch.object(BaseOAuth2, 'request_access_token')
    @mock.patch.object(TwitchOAuth2, 'user_data')
    def test_create_user(self, mock_user_data,
                         mock_request_access_token,
                         mock_validate_state):
        with step("environment setup"):
            #: you need same state as from Twitch backend has been received
            mock_validate_state.side_effect = ['FakeState']
            mock_request_access_token.side_effect = [self.auth_response]
            #: user data received from auth service
            mock_user_data.side_effect = [self.user_data]

        with step("authorization process OAuth2"):
            response = self.client.get(self.auth_url_complete,
                                       data=self.oauth_response, follow=True)
            self.assertEqual(response.status_code, HttpStatus.OK)
            context = response.context
            self.assertTrue(context['user'].is_authenticated)
