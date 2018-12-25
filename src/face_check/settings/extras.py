"""
This module keeps very simple plug-able interface to configure
project with extra project modules provided over setup.py
"""
import pkg_resources
from . import dist as default


def requires(dependencies, *, validator=all):
    """
    Checks if package has dependencies according to `validator` logic

    :param list[str] | tuple[str] dependencies: list of dependencies without
        its versions, for example: raven, requests, wheel, setuptools, etc
    :param callable validator: boolean sequence validator, by default it's
        :py:func:`all`. Recommended to use

        - :py:func:`all`
        - :py:func:`any`
    :return: decorator
    """
    distribution = pkg_resources.get_distribution('face-check')
    has_resource = distribution.has_resource

    def decorator(func):
        def wrapper(*args, **kwargs):
            have_all_dependencies = validator(map(has_resource, dependencies))
            if have_all_dependencies:
                return func(*args, **kwargs)
            return
        return wrapper
    return decorator


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
