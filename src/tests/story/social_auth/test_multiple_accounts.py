"""
This test case checks multiple login from different social networks
and basic corner cases.

.. note::

    Some of functionality has been tested over mocking real working api
    responses, it means changing this module requires much work and it's
    not counted as e2e test cases are desired.
"""
import json
from unittest import mock

from django.db.models import Q
from django.urls import reverse
from django.test import TestCase

from django.contrib.auth import get_user_model

from social_django.models import UserSocialAuth
from social_core.backends.twitch import TwitchOAuth2
from social_core.backends.google import GoogleOAuth2
from social_core.backends.oauth import OAuthAuth, BaseOAuth2

from face_check.consts import HttpStatus
from face_check.api.goodgame import GoodGameVerifier
from face_check.api.youtube import YoutubeVerifier
from face_check.api.twitch import TwitchVerifier
from face_check.social.backends.goodgame import GoodGameOAuth2

from . import step, OAuth2MockMixin
from .. fixtures.twitch import TWITCH_FOLLOWER_INFO
from ... import ResourceMixin, FakeResponse


class MultipleAccountsAuthTest(ResourceMixin, OAuth2MockMixin, TestCase):
    """
    whole pipeline:
    user -> twitch {auth} (complete) -> backend -> twitch {token} -> finish
    tested part started from complete push from twitch, emulated with mocks
    """
    oauth2_mock_scope = []

    @classmethod
    def setUpClass(cls):
        cls.user_model = get_user_model()
        cls.auth_urls_complete = {
            'goodgame': reverse("social:complete", args=("goodgame", )),
            'youtube': reverse('social:complete', args=('google-oauth2', )),
            'twitch': reverse('social:complete', args=('twitch', )),
        }
        cls.user_data = {
            'twitch': json.load(
                cls.get_resource('social_auth/user_data/twitch.json')
            ),
            'goodgame': json.load(
                cls.get_resource('social_auth/user_data/goodgame.json')
            ),
            'youtube': json.load(
                cls.get_resource('social_auth/user_data/youtube.json')
            )
        }

        #: setup aux
        good_game_channel_info = []
        for page in range(1, 4):
            with cls.get_resource('social_auth/channel_info/'
                                  'goodgame-page{}.json'.format(page)) as f:
                content = f.read()

            good_game_channel_info.append(FakeResponse(content=content))
        youtube_subscription = json.load(
            cls.get_resource('social_auth/channel_info/'
                             'youtube-subscription.json')
        )

        cls.aux = {
            'goodgame-channel_info': good_game_channel_info,
            'youtube-subscription': youtube_subscription,
            'twitch-follows': TWITCH_FOLLOWER_INFO
        }
        super().setUpClass()

    @mock.patch.object(OAuthAuth, 'validate_state')
    @mock.patch.object(BaseOAuth2, 'request_access_token')
    @mock.patch.object(GoodGameOAuth2, 'user_data')
    @mock.patch.object(GoogleOAuth2, 'user_data')
    @mock.patch.object(TwitchOAuth2, 'user_data')
    @mock.patch.object(GoodGameVerifier, '_get_channel_subscribers')
    @mock.patch.object(YoutubeVerifier, '_get_subscription')
    @mock.patch.object(TwitchVerifier, '_get_user_follow')
    def test_multiple_auth(self, mock_twitch_verifier,
                           mock_youtube_verifier,
                           mock_good_game_verifier,
                           mock_twitch_user_data,
                           mock_youtube_user_data,
                           mock_good_game_user_data,
                           mock_request_access_token,
                           mock_validate_state):
        with step("environment setup"):
            #: you need same state as from Twitch backend has been received
            mock_validate_state.return_value = 'FakeState'
            mock_request_access_token.return_value = self.auth_response
            #: user data received from auth service
            mock_good_game_user_data.return_value = self.user_data['goodgame']
            mock_youtube_user_data.return_value = self.user_data['youtube']
            mock_twitch_user_data.return_value = self.user_data['twitch']

            #: mocks get player information
            mock_twitch_verifier.return_value = self.aux['twitch-follows']
            mock_youtube_verifier.return_value = \
                self.aux['youtube-subscription']
            mock_good_game_verifier.side_effect = \
                self.aux['goodgame-channel_info']

        with step("Authentication process Twitch"):
            response = self.client.get(self.auth_urls_complete['twitch'],
                                       data=self.oauth_response, follow=True)
            self.assertEqual(response.status_code, HttpStatus.OK)
            context = response.context
            self.assertTrue(context['user'].is_authenticated)
            with step('check twitch social bound'):
                self.assertEqual(context['user'].email,
                                 'tarvitz@blacklibrary.ru')
            with step('logout'):
                self.client.logout()

        with step("Authentication process Youtube"):
            response = self.client.get(self.auth_urls_complete['youtube'],
                                       data=self.oauth_response, follow=True)
            self.assertEqual(response.status_code, HttpStatus.OK)
            context = response.context
            self.assertTrue(context['user'].is_authenticated)
            with step('check twitch social bound'):
                self.assertEqual(context['user'].email,
                                 'tarvitz@blacklibrary.ru')
            with step('logout'):
                self.client.logout()

        with step("Authentication process GoodGame"):
            response = self.client.get(self.auth_urls_complete['goodgame'],
                                       data=self.oauth_response, follow=True)
            self.assertEqual(response.status_code, HttpStatus.OK)
            context = response.context
            self.assertTrue(context['user'].is_authenticated)
            with step('check good game social bound'):
                self.assertNotEqual(context['user'].email,
                                    'tarvitz@blacklibrary.ru')

            with step('logout'):
                self.client.logout()

        with step("Check social backends bound to user"):
            #: note that each social backend should have to be linked into
            #: single user email, in case of face-check tarvitz@blacklibrary.ru
            #: email address is used.

            #: once good game returns email properly account will be associated
            #: twitch + good game explicitly check
            self.assertEqual(
                UserSocialAuth.objects.filter(provider='goodgame').count(),
                1
            )
            self.assertEqual(
                UserSocialAuth.objects.filter(provider='twitch').count(),
                1
            )
            self.assertEqual(
                UserSocialAuth.objects.filter(
                    provider='google-oauth2').count(),
                1
            )
        with step('check accounts association'):
            #: google and twitch should be associated with single internal
            #: user. (GG would be associated too as far as they provide
            #: email address in user details)
            social_account = UserSocialAuth.objects.filter(
                provider='twitch').get()
            user = social_account.user
            self.assertEqual(
                user.social_auth.filter(
                    Q(provider='twitch') | Q(provider='google-oauth2')
                ).count(),
                2
            )
