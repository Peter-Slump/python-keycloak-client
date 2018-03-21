import json

from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase


ROLE_KWARGS = ['description', 'id', 'client_role', 'composite', 'composites',
               'container_id', 'scope_param_required']


def to_camel_case(snake_cased_str):
    components = snake_cased_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(map(str.capitalize, components[1:]))


class Roles(KeycloakAdminBase):

    _client_id = None
    _realm_name = None
    _paths = {
        'collection': '/auth/admin/realms/{realm}/clients/{id}/roles'
    }

    def __init__(self, realm_name, client_id, *args, **kwargs):
        self._client_id = client_id
        self._realm_name = realm_name
        super(Roles, self).__init__(*args, **kwargs)

    def by_name(self, role_name):
        return Role(realm_name=self._realm_name, client_id=self._client_id,
                    role_name=role_name, client=self._client)

    def create(self, name, **kwargs):
        """
        Create new role

        http://www.keycloak.org/docs-api/3.4/rest-api/index.html#_roles_resource

        :param str name: Name for the role
        :param str description: (optional)
        :param str id: (optional)
        :param bool client_role: (optional)
        :param bool composite: (optional)
        :param object composites: (optional)
        :param str container_id: (optional)
        :param bool scope_param_required: (optional)
        """
        payload = OrderedDict(name=name)

        for key in ROLE_KWARGS:
            if key in kwargs:
                payload[to_camel_case(key)] = kwargs[key]

        return self._client.post(
            url=self._client.get_full_url(
                self.get_path('collection',
                              realm=self._realm_name,
                              id=self._client_id)
            ),
            data=json.dumps(payload)
        )


class Role(KeycloakAdminBase):

    _paths = {
        'single': '/auth/admin/realms/{realm}/clients/{id}/roles/{role_name}'
    }

    def __init__(self, realm_name, client_id, role_name, *args, **kwargs):
        self._client_id = client_id
        self._realm_name = realm_name
        self._role_name = role_name

        super(Role, self).__init__(*args, **kwargs)

    def update(self, name, **kwargs):
        """
        Update existing role.

        http://www.keycloak.org/docs-api/3.4/rest-api/index.html#_roles_resource

        :param str name: Name for the role
        :param str description: (optional)
        :param str id: (optional)
        :param bool client_role: (optional)
        :param bool composite: (optional)
        :param object composites: (optional)
        :param str container_id: (optional)
        :param bool scope_param_required: (optional)
        """
        payload = OrderedDict(name=name)

        for key in ROLE_KWARGS:
            if key in kwargs:
                payload[to_camel_case(key)] = kwargs[key]

        return self._client.put(
            url=self._client.get_full_url(
                self.get_path('single',
                              realm=self._realm_name,
                              id=self._client_id,
                              role_name=self._role_name)
            ),
            data=json.dumps(payload)
        )
