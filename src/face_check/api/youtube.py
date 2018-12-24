import requests

from datetime import datetime, timedelta

from . import base


class YoutubeVerifier(base.SimpleVerifier):
    def __init__(self, channel_id, access_token):
        self.channel_id = channel_id
        self.access_token = access_token
        self.headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }

    def _get_subscription(self):
        """
        Gets information if user is subscribed to channel

        :rtype: requests.Response
        :return: good game player information http api call result
        """
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/subscriptions',
            params={
                'part': 'snippet',
                'mine': 'true',
                'forChannelId': self.channel_id
            },
            headers=self.headers
        )
        if response.status_code == 200:
            return response.json()
        return {}

    def get_follower_info(self):
        """
        Get follower information from youtube api subscriptions

        :rtype: dict
        :return: follower info
        """
        payload = self._get_subscription()
        snippet = payload.get('items', [{}])[0].get('snippet', {})
        #: re-processing publishedAt
        if 'publishedAt' in snippet:
            snippet['publishedAt'] = datetime.strptime(
                snippet['publishedAt'],
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        else:
            #: if nothing has been found publishedAt set to future
            snippet['publishedAt'] = datetime.now() + timedelta(days=1)
        return snippet
