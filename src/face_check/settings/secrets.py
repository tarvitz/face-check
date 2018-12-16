#: configuration keeping secrets keys separately to keep them in strict
#: form

from . utils import get_env_string

SOCIAL_AUTH_TWITCH_KEY = get_env_string('SOCIAL_AUTH_TWITCH_KEY', '')
SOCIAL_AUTH_TWITCH_SECRET = get_env_string('SOCIAL_AUTH_TWITCH_SECRET', '')


def secrets_dummy():
    """
    dummy method :)
    """
