import json
from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase, KeycloakAdminEntity

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

        self._client.post(
            url=self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            ),
            data=json.dumps(payload, sort_keys=True)
        )
        users = self._client.get(
            url=self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            ),
            username=username
        )
        return User(realm_name=self._realm_name, user_id=users[0]["id"], client=self._client)

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


class User(KeycloakAdminEntity):
    _BASE = "/auth/admin/realms/{realm}/users/{user_id}"
    _paths = {
        'single': _BASE,
        'reset_password': _BASE + "/reset-password"
    }

    def __init__(self, realm_name, user_id, client):
        self._realm_name = realm_name
        self._user_id = user_id
        self._user = None
        super(User, self).__init__(url=self.get_path('single', realm=realm_name, user_id=user_id),
                                   client=client)

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

    def update(self, **kwargs):
        data = {**kwargs, "id": self._user_id}
        return super().update(**data)

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
