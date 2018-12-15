import os
import unittest

from unittest import mock
from face_check.settings import utils


class MockEnv(object):
    """
    Helps to override os.environment with your settings
    usage::

    >>> with MockEnv({'ENV': 'Me'}):
    ...    assert os.environ.get('ENV') == 'Me'
    """

    def __init__(self, override):
        """
        :param dict override: override os.environment
        """
        self.override = override
        self._event = None

    def __enter__(self):
        self._event = mock.patch.dict(os.environ, self.override)
        self._event.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._event.stop()
        return


class UtilsTestCase(unittest.TestCase):
    """
    Utils Common Test Case
    """

    def test_get_literal_eval(self):
        self.assertEqual(
            utils._get_literal_from_env("NON_EXISTENT", 'fallback'), 'fallback'
        )
        with MockEnv({
            'DICT': '{"a": 1}',
            'PYTHON_TYPE_ERROR': 'string',
            'PYTHON_STRING': '"string"'
        }):
            self.assertEqual(utils._get_literal_from_env('DICT', {}), {'a': 1})
            self.assertEqual(utils._get_literal_from_env(
                'PYTHON_TYPE_ERROR', 'fallback'), 'fallback'
            )
            self.assertEqual(utils._get_literal_from_env(
                'PYTHON_STRING', 'fallback'), 'string'
            )

    def test_get_env_fallback_assertion(self):
        with self.assertRaises(AssertionError):
            utils.get_env_bool("ENV", 'string')

        with self.assertRaises(AssertionError):
            utils.get_env_string("ENV", 1)

    def test_get_env_common(self):
        """
        tests get_env_string, get_env_bool, etc legit output
        """
        self.assertFalse(utils.get_env_bool('ENV', fallback=False))
        self.assertEqual(utils.get_env_string('ENV', fallback="fallback"),
                         "fallback")

    def test_rel(self):
        self.assertNotEqual(utils.rel('static'), '/static/')
