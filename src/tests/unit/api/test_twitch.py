import datetime

from unittest import mock

from django.conf import settings
from django.test import TestCase
from face_check.api.twitch import TwitchVerifier

from ... import ResourceMixin

_CHANNEL_INFO = {
    'mature': False,
    'status': '??MAP CONTEST CUP',
    'broadcaster_language': 'ru',
    'broadcaster_software': 'unknown_rtmp',
    'display_name': 'WellPlayedTV1',
    'game': 'Warcraft III: The Frozen Throne',
    'language': 'ru',
    'id': 17861167,
    'name': 'wellplayedtv1',
    'created_at': datetime.datetime(2010, 11, 15, 17, 14, 10, 348107),
    'updated_at': datetime.datetime(2018, 12, 15, 22, 53, 57, 816585),
    'partner': False,
    'logo': 'https://static-cdn.jtvnw.net/jtv_user_pictures/'
            'a9a8c73e-5d59-4e24-9631-02b704bd32b2-'
            'profile_image-300x300.jpg',
    'video_banner': (
        'https://static-cdn.jtvnw.net/'
        'jtv_user_pictures/a6e10375-ecab-4818-bbd8-8b68cb654b4d-'
        'channel_offline_image-1920x1080.jpg'
    ),
    'profile_banner': (
        'https://static-cdn.jtvnw.net/jtv_user_pictures/da54d541-'
        '5bf1-4360-9d17-2db97e47e595-profile_banner-480.jpg'
    ),
    'profile_banner_background_color': '#9c1919',
    'url': 'https://www.twitch.tv/wellplayedtv1',
    'views': 212060,
    'followers': 2662,
    'broadcaster_type': 'affiliate',
    'description': '',
    'private_video': False,
    'privacy_options_enabled': False
}


class TwitchTest(ResourceMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subscribed_valid = {
            'created_at': datetime.datetime(2018, 3, 12, 17, 56, 12),
            'channel': _CHANNEL_INFO,
            'notifications': True
        }
        cls.subscribed_invalid = {
            'created_at': datetime.datetime(2019, 1, 1),
            'channel': _CHANNEL_INFO,
            'notifications': True
        }
        super().setUpClass()

    def test_filters(self):
        verifier = TwitchVerifier(client_id=settings.SOCIAL_AUTH_TWITCH_KEY,
                                  uid=74767317, channel_id=17861167)
        with mock.patch.object(TwitchVerifier, '_get_user_follow',
                               side_effect=[self.subscribed_valid]):
            self.assertTrue(
                verifier.verify(created_at__lt=datetime.datetime(2019, 1, 1))
            )
        with mock.patch.object(TwitchVerifier, '_get_user_follow',
                               side_effect=[self.subscribed_invalid]):
            self.assertFalse(
                verifier.verify(created_at__lt=datetime.datetime(2019, 1, 1))
            )
