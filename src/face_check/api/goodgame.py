import requests

from . import filters


class GoodGameVerifier(object):
    def __init__(self, access_token, player_id):
        self.access_token = access_token
        self.player_id = player_id
    
    def _get_player_info(self):
        """
        Gets information for subscriber (through access_token)
        if user (access_token) is subscribed to selected
        player
        """
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        response = requests.get(
            'https://api2.goodgame.ru/player/{}'.format(self.player_id),
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        return {}

    def verify(self, **query):
        """
        Verifies if user is subscribed to channel id

        :rtype: bool
        :return: True if user passed subscribed follows validation
        """
        follows = self._get_player_info(player_id=self.player_id)
        if follows is None:
            return False

        #: straight forward validation pipeline
        return filters.and_expression(payload=follows, **query)
