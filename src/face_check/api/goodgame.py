import requests

from urllib import parse
from datetime import datetime, timedelta

from . import base, path


def _get_last_page(payload):
    """
    Get last page according to good game api response

    :param dict payload: good game api response
    :rtype: int
    :return: last page number
    """

    params = dict(
        parse.parse_qsl(
            parse.urlparse(
                path.traverse(payload, '_links.last.href'), '?page=1'
            ).query
        )
    )
    last_page = params.get('page') or '1'
    return int(last_page) if last_page.isdigit() else 1


class GoodGameVerifier(base.SimpleVerifier):
    """
    Half verifier - half small api base client for good game.
    Please don't extend internal API calls, once any severe modification
    of :py:class:`GoodGameVerifier` extend required please move everything
    related to Good Game API to separate class or set of classes
    """
    methods = {
        'channel_subscribers': '_get_channel_subscribers'
    }

    def __init__(self, access_token, uid, channel_id):
        self.access_token = access_token
        self.channel_id = channel_id
        self.uid = uid
        self.headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }

    def _get_channel_subscribers(self, *, page=1):
        """
        Gets information for subscriber (through access_token)
        if user (access_token) is subscribed to selected
        player

        :rtype: requests.Response
        :return: good game player information http api call result
        """
        response = requests.get(
            'https://api2.goodgame.ru/channel/{}/subscribers'.format(
                self.channel_id
            ),
            params={'page': page},
            headers=self.headers
        )
        return response

    def pages(self, method):
        """
        Iterate over paginated API responses

        :param str method: registered API method
        :rtype: list
        :return: list of embedded objects or empty
        """
        action = getattr(self, self.methods[method])
        response = action()
        if response.status_code == 200:
            payload = response.json()
            yield path.traverse(payload, '_embedded') or []

            last_page = _get_last_page(payload)
            for page in range(1, last_page + 1):
                response = action(page=page)
                content = (
                    response.json() if response.status_code == 200 else {}
                )
                yield path.traverse(content, '_embedded') or []
        raise StopIteration

    def get_follower_info(self):
        """
        Aggregate all subscribers from GG's API iterating through responses

        :rtype: dict
        :return: follower info
        """
        for page in self.pages(method='channel_subscribers'):
            for sub in page.get('subscribers', []):
                if sub.get('id', -1) == self.uid:
                    #: cheat :)
                    sub['created_at'] = float(sub['created_at'])
                    return sub
        #: in case if no one was found return follower looking like information
        #: with fake data to process, it's not good decision to fake it,
        #: however as part of simple verification it's better to keep it
        #: instead of making bunch of extra validations
        return {
            'uid': -1,
            'created_at': (datetime.now() + timedelta(days=1)).timestamp(),
            'username': 'not-found'
        }
