import json

from keycloak.admin import KeycloakAdminBase

__all__ = ('UserRoles',)


class UserRoles(KeycloakAdminBase):
    _paths = {
        'availableRealm': '/auth/admin/realms/{realm}/users/{id}' +
                          '/role-mappings/realm/available',
        'roleRealm': '/auth/admin/realms/{realm}/users/{id}' +
                     '/role-mappings/realm'
    }

    def __init__(self, realm_name, user_id, *args, **kwargs):
        self._realm_name = realm_name
        self._user_id = user_id
        super(UserRoles, self).__init__(*args, **kwargs)

    def available_realm_role(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    'availableRealm', realm=self._realm_name, id=self._user_id
                )
            )
        )

    def add_realm_role(self, roles):
        """
        :param roles: _rolerepresentation keycloak api
        """
        return self._client.post(
            url=self._client.get_full_url(
                self.get_path(
                    'roleRealm', realm=self._realm_name, id=self._user_id
                )
            ),
            data=json.dumps(roles)
        )
