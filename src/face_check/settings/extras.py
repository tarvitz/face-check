"""
This module keeps very simple plug-able interface to configure
project with extra project modules provided over setup.py
"""
from . import dist as default
from . utils import requires


@requires(['raven'], validator=all)
def setup_sentry():
    """
    Setup sentry configuration
    """
    default.INSTALLED_APPS.extend(['raven.contrib.django.raven_compat'])


def extras_setup():
    for key, obj in globals().items():
        if key.startswith('setup_') and callable(obj):
            obj()
