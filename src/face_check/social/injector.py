import logging
from django.conf import settings
from face_check.api import twitch, goodgame, youtube


logger = logging.getLogger(__file__)


def _verify_twitch(response, user):
    validator = twitch.TwitchVerifier(
        client_id=settings.SOCIAL_AUTH_TWITCH_KEY, uid=response.get('_id', 0),
        channel_id=settings.FACE_CHECK_CHANNEL['twitch']
    )
    is_verified = validator.verify(
        created_at__lte=settings.FACE_CHECK_DATE_OFFSET
    )
    user.is_verified = is_verified
    user.save()


def _verify_goodgame(uid, user, access_token):
    validator = goodgame.GoodGameVerifier(
        uid=uid,
        access_token=access_token,
        channel_id=settings.FACE_CHECK_CHANNEL['goodgame']
    )
    user.is_verified = validator.verify(
        created_at__lt=settings.FACE_CHECK_DATE_OFFSET.timestamp()
    )
    user.save()


def _verify_youtube(user, access_token):
    validator = youtube.YoutubeVerifier(
        channel_id=settings.FACE_CHECK_CHANNEL['youtube'],
        access_token=access_token
    )
    user.is_verified = validator.verify(
        publishedAt__lt=settings.FACE_CHECK_DATE_OFFSET
    )
    user.save()


def verify(backend, details, response, *args, **kwargs):
    user = kwargs['user']
    if user.is_verified:
        logger.info("User <%s> already verified" % repr(user))
        return {}

    access_token = kwargs['social'].access_token
    #: very straight forward processing services
    if backend.name == 'twitch':
        _verify_twitch(response, user=user)
    elif backend.name == 'goodgame':
        _verify_goodgame(uid=kwargs['uid'], user=user,
                         access_token=access_token)
    #: basically we use youtube, but google has its global authentication
    #: provider so this is it
    elif backend.name == 'google-oauth2':
        _verify_youtube(user=user, access_token=access_token)
    else:
        logger.warning("Unsupported backend, skipping")
    #: nothing to extend
    return {}
