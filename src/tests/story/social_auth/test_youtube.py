"""
This module test Good Game Auth with injections provided in projects
Basic goal to verify working settings.SOCIAL_AUTH_PIPELINE with
projects modifications.

.. note::

    Some of functionality has been tested over mocking real working api
    responses, it means changing this module requires much work and it's
    not counted as e2e test cases are desired.
"""
import json
from unittest import mock

from django.urls import reverse
from django.test import TestCase
from social_core.backends.oauth import OAuthAuth, BaseOAuth2
from social_core.backends.google import GoogleOAuth2

from face_check.consts import HttpStatus
from face_check.api.youtube import YoutubeVerifier

from . import step, OAuth2MockMixin

from ... import ResourceMixin


class YoutubeLoginTest(ResourceMixin, OAuth2MockMixin, TestCase):
    """
    whole pipeline:
    user -> twitch {auth} (complete) -> backend -> twitch {token} -> finish
    tested part started from complete push from twitch, emulated with mocks
    """
    oauth2_mock_scope = ['channel.subscribers']

    @classmethod
    def setUpClass(cls):
        cls.auth_url_complete = reverse("social:complete",
                                        args=("google-oauth2", ))

        #: google oauth response to /complete/goodgame/
        #: user profile data
        cls.user_data = json.load(
            cls.get_resource('social_auth/user_data/youtube.json')
        )
        cls.subscription = json.load(
            cls.get_resource('social_auth/channel_info/'
                             'youtube-subscription.json')
        )
        super().setUpClass()

    @mock.patch.object(OAuthAuth, 'validate_state')
    @mock.patch.object(BaseOAuth2, 'request_access_token')
    @mock.patch.object(GoogleOAuth2, 'user_data')
    @mock.patch.object(YoutubeVerifier, '_get_subscription')
    def test_create_user(self, mock_youtube_verifier,
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
            mock_youtube_verifier.return_value = self.subscription

        with step("authorization process OAuth2"):
            response = self.client.get(self.auth_url_complete,
                                       data=self.oauth_response, follow=True)
            self.assertEqual(response.status_code, HttpStatus.OK)
            context = response.context
            self.assertTrue(context['user'].is_authenticated)

            with step('check if verification passed and email extended'):
                self.assertTrue(context['user'].is_verified, True)
                self.assertEqual(context['user'].email,
                                 'tarvitz@blacklibrary.ru')
