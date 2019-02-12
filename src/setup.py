#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test

#: consider using setuptools_scm instead of declaring static version
version = "0.1"


class DjangoTest(test):
    user_options = [("django-test-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        test.initialize_options(self)
        self.django_test_args = ""

    def run_tests(self):
        import django
        from django.conf import settings
        from django.test.utils import get_runner

        os.environ['DJANGO_SETTINGS_MODULE'] = 'face_check.settings'
        django.setup()

        test_runner_class = get_runner(settings)
        #: django.test.runner.DiscoverRunner, additional options does not
        #: work for now
        test_runner = test_runner_class()
        failures = test_runner.run_tests(["tests"])
        sys.exit(bool(failures))


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Indented Audience :: System Administrators',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Natural Language :: English',
    'Topic :: Utilities',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.6'
]

install_requires = [
    #: BSD licenses
    'Django==2.1.6',
    'social-auth-app-django==3.1.0',
    'social-auth-core==2.0.0',
    #: MIT licenses
    'python-twitch-client==0.6.0'
]
test_requires = []


class ExtraRequirements(object):
    sentry = ['raven']
    #: all extra dependencies
    all = sentry


extras_require = {
    'all': ExtraRequirements.all,
    'sentry': ExtraRequirements.sentry,
}

setup(
    name='face-check',
    author='Nickolas Fox <tarvitz@blacklibrary.ru>',
    version=version,
    author_email='tarvitz@blacklibrary.ru',
    description='WellPlayed TV Face Check',
    long_description="",
    license='BSD',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=install_requires,
    test_requires=test_requires,
    packages=find_packages(
        exclude=('tests', 'resources')
    ),
    entry_points={
        'console_scripts': [
            'site-manage = face_check.manage:main',
            'wsgi-server = face_check.server.__main__:main'
        ]
    },
    package_data={
        '': ['templates/*', 'conf/*']
    },
    include_package_data=True,
    extras_require=extras_require,
    test_suite='tests',
    zip_safe=False,
    cmdclass={"django_test": DjangoTest}
)
