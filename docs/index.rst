.. Python Keycloak Client documentation master file, created by
   sphinx-quickstart on Wed Feb 21 19:29:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================================
Welcome to Python Keycloak Client's documentation!
==================================================

.. toctree::
   :maxdepth: 2

The `Python Keycloak Client <https://github.com/Peter-Slump/python-keycloak-client>`_
is a set of API clients written in Python to communicate with the different
API's which are exposed by `Keycloak <http://www.keycloak.org>`_.

Installation
============

.. code-block:: bash

    $ pip install git+https://github.com/Peter-Slump/python-keycloak-client.git

Preparation
===========

Make sure you have created a
`REALM <http://www.keycloak.org/docs/latest/server_admin/index.html#_create-realm>`_
and `Client <http://www.keycloak.org/docs/latest/server_admin/index.html#_clients>`_
in Keycloak.

Usage
=====

Everything starts with an instance of :class:`keycloak.realm.KeycloakRealm`

.. code-block:: python

    from keycloak.realm import KeycloakRealm


    realm = KeycloakRealm(server_url='https://example.com', server_url='my_realm')

--------------
OpenID Connect
--------------

The OpenID Connect entry point can be retrieved from the realm object.

.. code-block:: python

    from keycloak.realm import KeycloakRealm


    realm = KeycloakRealm(server_url='https://example.com', server_url='my_realm')

    oidc_client = realm.open_id_connect(client_id='my-client',
                                        client_secret='very-secret-client-secret')


.. automethod:: keycloak.openid_connect.KeycloakOpenidConnect.authorization_url

.. automethod:: keycloak.openid_connect.KeycloakOpenidConnect.authorization_code

.. automethod:: keycloak.openid_connect.KeycloakOpenidConnect.client_credentials

.. automethod:: keycloak.openid_connect.KeycloakOpenidConnect.refresh_token

.. automethod:: keycloak.openid_connect.KeycloakOpenidConnect.logout

.. automethod:: keycloak.openid_connect.KeycloakOpenidConnect.certs

.. automethod:: keycloak.openid_connect.KeycloakOpenidConnect.userinfo

------------------------------
Authz (Authorization services)
------------------------------

The Authz client can be retrieved from the realm object.

.. code-block:: python

    from keycloak.realm import KeycloakRealm


    realm = KeycloakRealm(server_url='https://example.com', server_url='my_realm')

    authz_client = realm.authz(client_id='my-client')


.. automethod:: keycloak.authz.KeycloakAuthz.entitlement

---------
Admin API
---------

Manage Realms, Clients, Roles, Users etc.

http://www.keycloak.org/docs-api/3.4/rest-api/index.html

The admin API client get be retrieved from the realm object.

.. code-block:: python

    from keycloak.realm import KeycloakRealm


    realm = KeycloakRealm(server_url='https://example.com', server_url='my_realm')

    admin_client = realm.admin

Realms
------

Currently there is no actual functionality available for Realm management.
However this endpoint is the entrypoint for all other clients.

.. code-block:: python

    realm = realm.admin.realms.by_name('realm-name')

Clients
-------

Manage clients

.. code-block:: python

    clients = realm.admin.realms.by_name('realm-name').clients

The following methods can be accessed:

.. automethod:: keycloak.admin.clients.Clients.all

Roles
-----

Manage client roles

.. code-block:: python

    roles = realm.admin.realms.by_name('realm-name').clients.by_id('#client id').roles

The following methods are available:

.. automethod:: keycloak.admin.roles.Roles.create

Actions on a specific role

.. code-block:: python

    role = realm.admin.realms.by_name('realm-name').clients.by_id('#client id').roles.by_name('role-name')

The following methods are available:

.. automethod:: keycloak.admin.roles.Role.update


Users
-----

Manage users in a REALM

.. code-block:: python

    users = realm.admin.realms.by_name('realm-name').users

The following methods are available:

.. automethod:: keycloak.admin.users.Users.create

-------------------------
UMA (User-Managed Access)
-------------------------

The UMA client can be retrieved from the realm object.

http://www.keycloak.org/docs/latest/authorization_services/index.html#_service_overview

.. code-block:: python

    from keycloak.realm import KeycloakRealm


    realm = KeycloakRealm(server_url='https://example.com', server_url='my_realm')

    uma_client = realm.uma()


Resource Set management
-----------------------

.. automethod:: keycloak.uma.KeycloakUMA.resource_set_create

.. automethod:: keycloak.uma.KeycloakUMA.resource_set_update

.. automethod:: keycloak.uma.KeycloakUMA.resource_set_read

.. automethod:: keycloak.uma.KeycloakUMA.resource_set_delete

.. automethod:: keycloak.uma.KeycloakUMA.resource_set_list


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

