#: configuration keeping secrets keys separately to keep them in strict
#: form

#: reduce redundant imports
from . utils import get_env_string as _get_env_string

SOCIAL_AUTH_TWITCH_KEY = _get_env_string('SOCIAL_AUTH_TWITCH_KEY', '')
SOCIAL_AUTH_TWITCH_SECRET = _get_env_string('SOCIAL_AUTH_TWITCH_SECRET', '')
SOCIAL_AUTH_GOODGAME_KEY = _get_env_string('SOCIAL_AUTH_GOODGAME_KEY', '')
SOCIAL_AUTH_GOODGAME_SECRET = _get_env_string('SOCIAL_AUTH_GOODGAME_SECRET',
                                              '')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = _get_env_string(
    'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', ''
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = _get_env_string(
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', ''
)
