import logging
from django.conf import settings
from face_check.api import twitch

logger = logging.getLogger(__file__)


def _verify_twitch(response, user):
    validator = twitch.TwitchVerifier(
        client_id=settings.SOCIAL_AUTH_TWITCH_KEY, uid=response.get('_id', 0),
        channel_id=settings.TWITCH_FACE_CHECK_CHANNEL
    )
    is_verified = validator.verify(
        created_at__lte=settings.FACE_CHECK_DATE_OFFSET
    )
    if user is not None:
        user.is_verified = is_verified
        user.save()


def verify(backend, details, response, *args, **kwargs):
    user = kwargs['user']
    if user.is_verified:
        logger.info("User <%s> already verified" % repr(user))
        return {}

    #: very straight forward processing services
    if backend.name == 'twitch':
        _verify_twitch(response, user=user)
    else:
        logger.warning("Unsupported backend, skipping")
    #: nothing to extend
    return {}
