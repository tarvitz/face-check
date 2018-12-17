"""
This module test Good Game Auth with injections provided in projects
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

from face_check.consts import HttpStatus
from face_check.api.goodgame import GoodGameVerifier
from face_check.social.backends.goodgame import GoodGameOAuth2

from . import step


class GoodGameLoginTest(TestCase):
    """
    whole pipeline:
    user -> twitch {auth} (complete) -> backend -> twitch {token} -> finish
    tested part started from complete push from twitch, emulated with mocks
    """
    @classmethod
    def setUpClass(cls):
        cls.auth_url_complete = reverse("social:complete", args=("goodgame", ))
        super().setUpClass()

    def setUp(self):
        #: google oauth response to /complete/twitch/
        self.oauth_response = {
            'code': 'ih2o4ibvirjxipejc19cevcp6b0939',
            'scope': 'channel.subscribers',
            'state': 'FakeState'
        }
        self.auth_response = {
            'access_token': '1e84e29qi5u2gozvoqaoebauwnd90n',
            'expires_in': 13048,
            'refresh_token': 'wrrjc22jp1gjm1irld1iklvaaaq1j77pemhgsi8pye6x1hlrdy',
            'scope': ['channel.subscribers'],
            'token_type': 'bearer'
        }
        
        #: user profile data
        self.user_data = {
            "token": {"scopes": ["channel.subscribers"], "expires": 1545159705},
            "user": {"user_id": "1013883", "username": "nickolasfox"},
            "channel": {"channel": None, "channel_id": None, "src": None},
            "_links": {"self": {"href": "https://api2.goodgame.ru/info"}}
        }

        #: verified data upon face-check channel used
        self.player_data = {
            "channel_id": "1850",
            "channel_key": "Enillydd",
            "channel_title": "💾26 на Battlenet до НГ !Challenge",
            "channel_status": "offline",
            "channel_poster": "https://goodgame.ru/files/logotypes/ch_1850_cKaf_orig.jpg",
            "channel_premium": True,
            "streamer_name": "WellPlayedTV",
            "streamer_avatar": "https://goodgame.ru/files/avatars/av_22909_LV3Z.jpg",
            "premium_only": False,
            "adult": 0,
            "channel_start": "1545043111",
            "ga_code": "",
            "broadcast": [],
            "user": {
                "premium_key": "PREMIUMKEYHASH",
                "premium_channel": "single",
                "days_left": 149,
                "expire": "1557939371",
                "test": False,
                "user_id": "1013883",
                "email": "tarvitz@blacklibrary.ru",
                "payments": 0,
                "subscribed": True,
                "subscribed_stream": True,
                "subscribed_anons": False
            },
            "_links": {"self": {"href": "https://api2.goodgame.ru/player/1850"}}
        }

    @mock.patch.object(OAuthAuth, 'validate_state')
    @mock.patch.object(BaseOAuth2, 'request_access_token')
    @mock.patch.object(GoodGameOAuth2, 'user_data')
    @mock.patch.object(GoodGameVerifier, '_get_player_info')
    def test_create_user(self, mock_good_game_verifier,
                         mock_user_data,
                         mock_request_access_token,
                         mock_validate_state):
        with step("environment setup"):
            #: you need same state as from Twitch backend has been received
            mock_validate_state.side_effect = ['FakeState']
            mock_request_access_token.side_effect = [self.auth_response]
            #: user data received from auth service
            mock_user_data.side_effect = [self.user_data]

            #: mocks get player information
            mock_good_game_verifier.side_effect = [self.player_data]

        with step("authorization process OAuth2"):
            response = self.client.get(self.auth_url_complete,
                                       data=self.oauth_response, follow=True)
            self.assertEqual(response.status_code, HttpStatus.OK)
            context = response.context
            self.assertTrue(context['user'].is_authenticated)
