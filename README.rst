Face Check
==========

.. contents::
  :local:
  :depth: 2

Purpose
-------
This is simple project written on django and python-social-auth to check user if he/she was subscribed / followed streamer channel for some long time

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


To install application into kubernetes you would simply need to run:

.. code-block:: bash

    #$ kubectl apply -f k8s/install.yaml

Development
~~~~~~~~~~~

To build current version of application simple run `./hack/build.sh`.

.. note::

    You will require `winpty <https://github.com/rprichard/winpty>`_
    if you run it on Windows Msys (git for windows base environment)
