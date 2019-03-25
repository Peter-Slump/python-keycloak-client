import json
from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase

__all__ = ('Users',)

USER_KWARGS = [
    'email',
    'firstName',
    'lastName',
    'emailVerified',
    'attributes',
    'realmRoles',
    'clientRoles',
    'groups'
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
        'single': '/auth/admin/realms/{realm}/users/{user_id}',
        'group': '/auth/admin/realms/{realm}/users/{user_id}/groups',
        'groupAdd': '/auth/admin/realms/{realm}/users/{user_id}/groups/{group_id}'
    }

    def __init__(self, realm_name, user_id, *args, **kwargs):
        self._realm_name = realm_name
        self._user_id = user_id
        self._it = None
        super(User, self).__init__(*args, **kwargs)

    @property
    def it(self):
        if self._it is None:
            self.get()
        return self._it

    def roles(self):
        from keycloak.admin.clientroles import ClientRoles
        return ClientRoles(realm_name=self._realm_name, user_id=self._user_id, client=self._client)

    def get(self):
        """
        Return registered user with the given user id.

        http://www.keycloak.org/docs-api/3.4/rest-api/index.html#_users_resource
        """
        self._it = self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    'single', realm=self._realm_name, user_id=self._user_id
                )
            )
        )
        self._user_id = self.it["id"]
        return self._it

    def update(self, **kwargs):
        """
                Update existing user.

                https://www.keycloak.org/docs-api/2.5/rest-api/index.html#_userrepresentation

                :param str firstName: Firstname for user
                :param str lastName: LastName for user
                :param str email: Email for user
                :param bool emailVerified: User email verified
                :param Map attributes: Atributes in user
                :param string array realmRoles: Realm Roles
                :param Map clientRoles: Client Roles
                :param string array groups: Groups for user
                """
        payload = OrderedDict()
        for k, v in self.it.items():
            payload[k] = v
        for key in USER_KWARGS:
            from keycloak.admin.clientroles import to_camel_case
            if key in kwargs:
                payload[to_camel_case(key)] = kwargs[key]
        print("*DEBUG* Update User:" + str(json.dumps(payload)))
        result = self._client.put(
            url=self._client.get_full_url(
                self.get_path(
                    'single', realm=self._realm_name, user_id=self._user_id
                )
            ),
            data=json.dumps(payload)
        )
        self.get()
        return result

    def user_groups(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    'group',
                    realm=self._realm_name,
                    user_id=self._user_id
                )
            )
        )

    def add_to_group(self, group_id):
        return self._client.put(
            url=self._client.get_full_url(
                self.get_path(
                    'groupAdd',
                    realm=self._realm_name,
                    user_id=self._user_id,
                    group_id=group_id
                )
            ),
            data=json.dumps({
                "realm": self._realm_name,
                "userId": self._user_id,
                "groupId": group_id
            })
        )

    def delete_group(self, group_id):
        return self._client.delete(
            url=self._client.get_full_url(
                self.get_path(
                    'groupAdd',
                    realm=self._realm_name,
                    user_id=self._user_id,
                    group_id=group_id
                )
            )
        )
