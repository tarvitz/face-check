"""
Fixtures for test cases, that's easy to import python way instead
of using json
"""

import datetime

TWITCH_FOLLOWER_INFO = {
    'created_at': datetime.datetime(2018, 3, 12, 17, 56, 12),
    'channel': {
        'mature': False,
        'status': '💾Ready to WORK !Challenge',
        'broadcaster_language': 'ru',
        'broadcaster_software': 'unknown_rtmp',
        'display_name': 'WellPlayedTV1',
        'game': 'Warcraft III: The Frozen Throne',
        'language': 'ru',
        'id': 17861167,
        'name': 'wellplayedtv1',
        'created_at': datetime.datetime(2010, 11, 15, 17, 14, 10, 348107),
        'updated_at': datetime.datetime(2018, 12, 24, 16, 31, 55, 706160),
        'partner': False,
        'logo': 'https://static-cdn.jtvnw.net/jtv_user_pictures/'
                'a9a8c73e-5d59-4e24-9631-02b704bd32b2-profile_'
                'image-300x300.jpg',
        'video_banner': 'https://static-cdn.jtvnw.net/jtv_user_pictures/'
                        'a6e10375-ecab-4818-bbd8-8b68cb654b4d-channel_'
                        'offline_image-1920x1080.jpg',
        'profile_banner': 'https://static-cdn.jtvnw.net/jtv_user_pictures/'
                          'da54d541-5bf1-4360-9d17-2db97e47e595-'
                          'profile_banner-480.jpg',
        'profile_banner_background_color': '#9c1919',
        'url': 'https://www.twitch.tv/wellplayedtv1',
        'views': 213475,
        'followers': 2668,
        'broadcaster_type': 'affiliate',
        'description': (
            'Добро пожаловать, на этом канале ты увидишь как можно улучшать '
            'свой скилл в любой игре несмотря на все препятствия, '
            'которые возникнут '
        ),
        'private_video': False,
        'privacy_options_enabled': False
    },
    'notifications': True
}
