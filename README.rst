WellPlayedTV Face Check
=======================

.. contents::
  :local:
  :depth: 2

Purpose
-------
This is simple project written on django and python-social-auth to check user if he/she was subscribed / followed streamer channel for some long time. Once user
is verified he/she is available to see some secret information left by administration.

Such information could be connection data, passwords to connect for game sessions,
or anything that administration would like to keep in secret and can not delegate
to his public services.

The basic idea was to share connection passwords for Warhammer 40000: Dawn of War Soulstorm championship among followers, however there was no any good and reliable channel to communicate with followers/subscribers.


Installation
------------
You would need:

- `Python-3.6 <https://www.python.org/downloads/>`_

Optional dependencies:

- `PostgreSQL 9.x <https://www.postgresql.org/download/>`_ + (could probably work on 8.4 + versions)


Kubernetes
~~~~~~~~~~

You have to get configured for your kubernetes cluster before:

- `rbac <https://kubernetes.io/docs/reference/access-authn-authz/rbac/>`_
- `ingress <https://kubernetes.io/docs/concepts/services-networking/ingress/>`_


To install application into kubernetes you would simply need to apply
kubernetes resources that stored into **k8s** directory. However you have to configure:

- k8s/configmap.yaml it's used for application configuration
- k8s/secret.yaml (note this file is absent in repository you have to create your own and apply it. read details below)
- k8s/deployment.yaml, you would probably like to change image registry as far as current image is store to the private one.

secret.yaml
```````````
To pass secret configuration for application simply create secret.yaml file with following configuration:

.. code-block:: yaml

    apiVersion: v1
    kind: Secret
    metadata:
      labels:
        app: face-check
      name: face-check
      namespace: face-check
    data:
      SOCIAL_AUTH_TWITCH_KEY: "<base64 encoded secret>"
      SOCIAL_AUTH_TWITCH_SECRET: "<base64 encoded secret>"
      SOCIAL_AUTH_GOODGAME_KEY: "<base64 encoded secret>"
      SOCIAL_AUTH_GOODGAME_SECRET: "<base64 encoded secret>"
      SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: "<base64 encoded secret>"
      SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: "<base64 encoded secret>"
      DATABASE_PASSWORD: "<base64 encoded secret>"

**<base64 encoded secret>** is a secret you have to encode in base64, for example
if your database password is **fooExample** you need to encode it:

.. code-block:: text

    #$ echo -n fooExample | base64
    Zm9vRXhhbXBsZQ==  # <-- this is your string you have to use

Building
~~~~~~~~

To build current version of application simple run `./hack/build.sh`.

.. note::

    You will require `winpty <https://github.com/rprichard/winpty>`_
    if you run it on Windows Msys (git for windows base environment)

Extra Dependencies
``````````````````
Passing *--build-arg=PIP_EXTRA_DEPENDENCIES=extras* will allow you to install extra project dependencies you won't probably need out of a box.

If you if you want to install with all extra dependencies

Here's supported list of dependencies:

- **all**, enables all extra dependencies listed below.
- **raven**, enables `sentry <https://getsentry.com>`_ logging

Example::

    $ ./hack/build.sh --build-arg="PIP_EXTRA_DEPENDENCIES=raven"

Tests
~~~~~
This project includes bunch of unit and story (i.e integration or functional) test
cases. They all placed separately from sources to minify extra actions application
building. You can run it using django test runner:

.. code-block:: text

    #: change directory to sources root:
    $ cd src/

    #: run test cases
    $ PYTHONPATH=. python face_check/manage.py test tests

The most sophisticated and useful test cases are stored into tests/story, they
check if application business logic works properly. However complexity of its
support and development is pretty high, so keep it in the mind in case if you'd
like to change your pipelines.
