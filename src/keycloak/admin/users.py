import json
from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase

__all__ = ('Users', 'User',)

USER_KWARGS = [
    'email',
    'first_name',
    'last_name',
    'email_verified',
    'attributes',
    'realm_roles',
    'client_roles',
    'groups',
    'enabled',
    'credentials'
]


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

        for key in USER_KWARGS:
            from keycloak.admin.clientroles import to_camel_case
            if key in kwargs:
                payload[to_camel_case(key)] = kwargs[key]

        return self._client.post(
            url=self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            ),
            data=json.dumps(payload, sort_keys=True)
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
    _BASE = "/auth/admin/realms/{realm}/users/{user_id}"
    _paths = {
        'single': _BASE,
        'reset_password': _BASE + "/reset-password"
    }

    def __init__(self, realm_name, user_id, *args, **kwargs):
        self._realm_name = realm_name
        self._user_id = user_id
        self._user = None
        super(User, self).__init__(*args, **kwargs)

    @property
    def user(self):
        if self._user is None:
            self.get()
        return self._user

    @property
    def role_mappings(self):
        from keycloak.admin.user.userroles import UserRoleMappings
        return UserRoleMappings(realm_name=self._realm_name,
                                user_id=self._user_id,
                                client=self._client)

    @property
    def groups(self):
        from keycloak.admin.user.usergroup import UserGroups
        return UserGroups(realm_name=self._realm_name,
                          user_id=self._user_id,
                          client=self._client)

    def get(self):
        """
        Return registered user with the given user id.

        http://www.keycloak.org/docs-api/3.4/rest-api/index.html#_users_resource
        """
        self._user = self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    'single', realm=self._realm_name, user_id=self._user_id
                )
            )
        )
        self._user_id = self.user["id"]
        return self._user

    def update(self, **kwargs):
        """
        Update existing user.

        https://www.keycloak.org/docs-api/2.5/rest-api/index.html#_userrepresentation

        :param str first_name: first_name for user
        :param str last_name: last_name for user
        :param str email: Email for user
        :param bool email_verified: User email verified
        :param Map attributes: Atributes in user
        :param string array realm_roles: Realm Roles
        :param Map client_roles: Client Roles
        :param string array groups: Groups for user
        """
        payload = {}
        for k, v in self.user.items():
            payload[k] = v
        for key in USER_KWARGS:
            from keycloak.admin.clientroles import to_camel_case
            if key in kwargs:
                payload[to_camel_case(key)] = kwargs[key]
        result = self._client.put(
            url=self._client.get_full_url(
                self.get_path(
                    'single', realm=self._realm_name, user_id=self._user_id
                )
            ),
            data=json.dumps(payload, sort_keys=True)
        )
        self.get()
        return result

    def delete(self):
        """
        Delete registered user with the given user id.
        """
        self._user = self._client.delete(
            url=self._client.get_full_url(
                self.get_path(
                    'single', realm=self._realm_name, user_id=self._user_id
                )
            )
        )

    def reset_password(self, password, temporary=False):
        payload = {
            "type": "password",
            "value": password,
            "temporary": temporary
        }
        result = self._client.put(
            url=self._client.get_full_url(
                self.get_path(
                    'reset_password', realm=self._realm_name,
                    user_id=self._user_id
                )
            ),
            data=json.dumps(payload, sort_keys=True)
        )
        return result
