======================
Python Keycloak Client
======================

.. image:: https://travis-ci.org/Peter-Slump/python-keycloak-client.svg?branch=master
   :target: https://travis-ci.org/Peter-Slump/python-keycloak-client
   :alt: Build Status
.. image:: https://readthedocs.org/projects/python-keycloak-client/badge/?version=latest
   :target: http://python-keycloak-client.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://codecov.io/gh/Peter-Slump/python-keycloak-client/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Peter-Slump/python-keycloak-client
   :alt: codecov
.. image:: https://api.codeclimate.com/v1/badges/30e837f8c737b5b3e120/maintainability
   :target: https://codeclimate.com/github/Peter-Slump/python-keycloak-client/maintainability
   :alt: Maintainability

.. image:: https://img.shields.io/pypi/l/python-keycloak-client.svg
   :target: https://pypi.python.org/pypi/python-keycloak-client
   :alt: License
.. image:: https://img.shields.io/pypi/v/python-keycloak-client.svg
   :target: https://pypi.python.org/pypi/python-keycloak-client
   :alt: Version
.. image:: https://img.shields.io/pypi/wheel/python-keycloak-client.svg
   :target: https://pypi.python.org/pypi/python-keycloak-client
   :alt: Wheel


Python Client for Keycloak identity and access management service

`Documentation <http://python-keycloak-client.readthedocs.io/en/latest/>`_

http://www.keycloak.org/

https://github.com/Peter-Slump/python-keycloak-client

Development
===========

Install development environment:

.. code:: bash

  $ make install-python

------------
Writing docs
------------

Documentation is written using Sphinx and maintained in the docs folder.

To make it easy to write docs Docker support is available.

First build the Docker container:

.. code:: bash

    $ docker build . -f DockerfileDocs -t python-keycloak-client-docs

Run the container

.. code:: bash

    $ docker run -v `pwd`:/src --rm -t -i -p 8050:8050 python-keycloak-client-docs

Go in the browser to http://localhost:8050 and view the documentation which get
refreshed and updated on every update in the documentation source.

--------------
Create release
--------------

.. code:: bash

    $ git checkout master
    $ git pull
    -- Update release notes --
    $ bumpversion release
    $ make deploy-pypi
    $ bumpversion --no-tag patch
    $ git push origin master --tags

Release Notes
=============

**unreleased**
**v0.2.3**

* Bug fix: `client_class` on `KeycloakRealm` constructor (thanks to `pcaro <https://github.com/pcaro>`_)
* Improve Keycloak Client (thanks to `ByJacob <https://github.com/ByJacob>`_)

    * add delete in admin client
    * add manage groups in realm
    * add manage user roles
    * rename Roles to ClientRoles

**v0.2.2**

* Added support for UMA1 for Keycloak < 4.0
* Allow to query registered users (thanks to `aberres <https://github.com/aberres>`_)

**v0.2.1**

* Including aio version in released package. (thanks to `mackeyja92 <https://github.com/mackeyja92>`_)

**v0.2.0**

* Added async client based on aiohttp (thanks to `nkoshell <https://github.com/nkoshell>`_)

**v0.1.4**

* Add support for password grant (thanks to `scranen <https://github.com/scranen>`_)
* Bugfix: Prevent multiple values for keyword argument 'audience' in jwt.decode() (thanks to `eugenejo <https://github.com/eugenejo>`_)