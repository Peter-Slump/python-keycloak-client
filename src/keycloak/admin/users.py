import json
from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase

__all__ = ('Users',)


class Users(KeycloakAdminBase):
    _paths = {
        'collection': '/auth/admin/realms/{realm}/users'
    }

    _realm_name = None

    def __init__(self, realm_name, *args, **kwargs):
        self._realm_name = realm_name
        super(Users, self).__init__(*args, **kwargs)

    def create(self, username, **kwargs):
        """
        Create a user in Keycloak

        http://www.keycloak.org/docs-api/3.4/rest-api/index.html#_users_resource

        :param str username:
        :param object credentials: (optional)
        :param str first_name: (optional)
        :param str last_name: (optional)
        :param str email: (optional)
        :param boolean enabled: (optional)
        """
        payload = OrderedDict(username=username)

        if 'credentials' in kwargs:
            payload['credentials'] = [kwargs['credentials']]

        if 'first_name' in kwargs:
            payload['firstName'] = kwargs['first_name']

        if 'last_name' in kwargs:
            payload['lastName'] = kwargs['last_name']

        if 'email' in kwargs:
            payload['email'] = kwargs['email']

        if 'enabled' in kwargs:
            payload['enabled'] = kwargs['enabled']

        return self._client.post(
            url=self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            ),
            data=json.dumps(payload)
        )

    def all(self):
        """
        Return all registered users

        http://www.keycloak.org/docs-api/3.4/rest-api/index.html#_users_resource
        """
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            )
        )

    def by_id(self, user_id):
        return User(realm_name=self._realm_name,
                    user_id=user_id, client=self._client)


class User(KeycloakAdminBase):
    _paths = {
        'single': '/auth/admin/realms/{realm}/users/{user_id}'
    }

    def __init__(self, realm_name, user_id, *args, **kwargs):
        self._realm_name = realm_name
        self._user_id = user_id

        super(User, self).__init__(*args, **kwargs)

    def get(self):
        """
        Return registered user with the given user id.

        http://www.keycloak.org/docs-api/3.4/rest-api/index.html#_users_resource
        """
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    'single', realm=self._realm_name, user_id=self._user_id
                )
            )
        )
