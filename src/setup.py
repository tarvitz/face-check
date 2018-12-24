#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = "0.1"

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
    'Django==2.1.4',
    'social-auth-app-django==3.1.0',
    #: MIT licenses
    'python-twitch-client==0.6.0'
]

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
    packages=find_packages(
        exclude=['tests', 'requirements', 'resources']
    ),
    entry_points={
        'console_scripts': [
            'site-manage = face_check.manage:main',
        ]
    },
    test_suite='tests',
    zip_safe=False
)
