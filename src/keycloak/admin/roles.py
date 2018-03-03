import json

from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase


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

    def create(self, name, description=None, id=None, client_role=None,
               composite=None, composites=None, container_id=None,
               scope_param_required=None):
        payload = OrderedDict(name=name)

        if description is not None:
            payload['description'] = description

        if id is not None:
            payload['id'] = id

        if client_role is not None:
            payload['clientRole'] = client_role

        if composite is not None:
            payload['composite'] = composite

        if composites is not None:
            payload['composites'] = composites

        if container_id is not None:
            payload['containerId'] = container_id

        if scope_param_required is not None:
            payload['scopeParamRequired'] = scope_param_required

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

    def update(self, name, description=None, id=None, client_role=None,
               composite=None, composites=None, container_id=None,
               scope_param_required=None):
        payload = OrderedDict(name=name)

        if description is not None:
            payload['description'] = description

        if id is not None:
            payload['id'] = id

        if client_role is not None:
            payload['clientRole'] = client_role

        if composite is not None:
            payload['composite'] = composite

        if composites is not None:
            payload['composites'] = composites

        if container_id is not None:
            payload['containerId'] = container_id

        if scope_param_required is not None:
            payload['scopeParamRequired'] = scope_param_required

        return self._client.put(
            url=self._client.get_full_url(
                self.get_path('single',
                              realm=self._realm_name,
                              id=self._client_id,
                              role_name=self._role_name)
            ),
            data=json.dumps(payload)
        )
