import os

_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RESOURCE_DIR = os.path.join(_BASE_DIR, 'resources/tests')


class ResourceMixin(object):
    @staticmethod
    def get_resource_path(rel_path):
        """
        Gets resource according to resources dir bound in package

        :param str rel_path: related path started from resource dir
        :rtype: str
        :return: path to resource
        """
        return os.path.join(RESOURCE_DIR, rel_path)

    @staticmethod
    def get_resource(rel_path, mode='rb'):
        """
        Gets resource file object according to resources dir bound in package

        :param str rel_path: related path started from resource dir
        :param str mode: file open mode
        :rtype: io.TextIOWrapper
        :return: path to resource
        """
        return open(ResourceMixin.get_resource_path(rel_path), mode)
