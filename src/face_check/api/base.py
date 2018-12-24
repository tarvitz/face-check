import abc
from . import filters


class SimpleVerifier(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_follower_info(self):
        """get followers to verify them"""

    def verify(self, **query):
        """
        Verifies if user is subscribed to channel id

        :rtype: bool
        :return: True if user passed subscribed follows validation
        """
        follower = self.get_follower_info()
        return filters.and_expression(follower, **query)
