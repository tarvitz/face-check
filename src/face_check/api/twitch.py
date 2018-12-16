"""
Module shortcuts and abbreviations:

- `op` is always for operator/operators,
  applies on other keywords, for example `op_map` means operators_map
- uid is for user identifier or user id

"""
import twitch
import requests.models

from . import filters


class TwitchVerifier(object):
    """
    >>> from datetime import datetime
    >>> offset = datetime(2019, 1, 1)
    >>> TwitchVerifier(client_id=..., uid=...,
    ...                channel_id=...).verify(created_at__lte=offset)
    """

    def __init__(self, client_id, uid, channel_id):
        self.uid = uid
        self.channel_id = channel_id

        self._user_follows_cache = None
        self._client = twitch.TwitchClient(client_id=client_id)

    def _get_user_follow(self, user_id, channel_id, *, use_cache=True):
        """
        Gets user (`user_id`) follow information for requested `channel_id`

        :param int user_id:
        :param int channel_id:
        :param bool use_cache: if True, takes already received information
            otherwise re-fetches it from API
        :rtype: dict | None
        :return: None
        """
        if self._user_follows_cache and not use_cache:
            return self._user_follows_cache
        try:
            self._user_follows_cache = self._client.users.\
                check_follows_channel(user_id=user_id, channel_id=channel_id)
            return self._user_follows_cache
        except requests.models.HTTPError:
            return None

    def verify(self, **query):
        """
        Verifies if user is subscribed to channel id

        :rtype: bool
        :return: True if user passed subscribed follows validation
        """
        follows = self._get_user_follow(user_id=self.uid,
                                        channel_id=self.channel_id)
        if follows is None:
            return False

        #: straight forward validation pipeline
        return filters.and_expression(payload=follows, **query)
