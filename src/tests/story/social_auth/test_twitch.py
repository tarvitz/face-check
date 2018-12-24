"""
This module test Twitch Auth with injections provided in projects
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
from social_core.backends.twitch import TwitchOAuth2

from face_check.consts import HttpStatus
from face_check.api.twitch import TwitchVerifier

from . import step, OAuth2MockMixin
from .. fixtures.twitch import TWITCH_FOLLOWER_INFO
from ... import ResourceMixin


class TwitchLoginTest(ResourceMixin, OAuth2MockMixin, TestCase):
    """
    whole pipeline:
    user -> twitch {auth} (complete) -> backend -> twitch {token} -> finish
    tested part started from complete push from twitch, emulated with mocks
    """
    oauth2_mock_scope = 'user_read'

    @classmethod
    def setUpClass(cls):
        cls.auth_url_complete = reverse("social:complete", args=("twitch", ))

        #: google oauth response to /complete/twitch/
        cls.user_data = json.load(
            cls.get_resource('social_auth/user_data/twitch.json')
        )
        super().setUpClass()

    @mock.patch.object(OAuthAuth, 'validate_state')
    @mock.patch.object(BaseOAuth2, 'request_access_token')
    @mock.patch.object(TwitchOAuth2, 'user_data')
    @mock.patch.object(TwitchVerifier, '_get_user_follow')
    def test_create_user(self, mock_twitch_verifier,
                         mock_user_data,
                         mock_request_access_token,
                         mock_validate_state):
        with step("environment setup"):
            #: you need same state as from Twitch backend has been received
            mock_validate_state.side_effect = ['FakeState']
            mock_request_access_token.side_effect = [self.auth_response]
            #: user data received from auth service
            mock_user_data.side_effect = [self.user_data]

            #: follower info
            mock_twitch_verifier.return_value = TWITCH_FOLLOWER_INFO

        with step("authorization process OAuth2"):
            response = self.client.get(self.auth_url_complete,
                                       data=self.oauth_response, follow=True)
            self.assertEqual(response.status_code, HttpStatus.OK)
            context = response.context
            self.assertTrue(context['user'].is_authenticated)
