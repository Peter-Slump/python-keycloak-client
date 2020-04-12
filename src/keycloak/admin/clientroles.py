import json
from collections import OrderedDict
from typing import Any, Dict

from keycloak.admin.base import to_camel_case
from keycloak.client import JSONType

from . import KeycloakAdminBase, KeycloakAdminEntity

ROLE_KWARGS = [
    "description",
    "id",
    "client_role",
    "composite",
    "composites",
    "container_id",
    "scope_param_required",
]

__all__ = ("ClientRole", "ClientRoles")


class ClientRoles(KeycloakAdminBase):

    _paths: Dict[str, str] = {
        "collection": "/auth/admin/realms/{realm}/clients/{id}/roles"
    }

    def __init__(self, realm_name: str, client_id: str, *args: Any, **kwargs: Any):
        self._client_id: str = client_id
        self._realm_name: str = realm_name
        super().__init__(*args, **kwargs)

    def all(self) -> JSONType:
        return self._client.get(
            self._client.get_full_url(
                self.get_path("collection", realm=self._realm_name, id=self._client_id)
            )
        )

    def by_name(self, role_name: str) -> "ClientRole":
        return ClientRole(
            realm_name=self._realm_name,
            client_id=self._client_id,
            role_name=role_name,
            client=self._client,
        )

    def create(self, name: str, **kwargs: Any) -> JSONType:
        """
        Create new role

        http://www.keycloak.org/docs-api/3.4/rest-api/index.html
        #_roles_resource

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
                self.get_path("collection", realm=self._realm_name, id=self._client_id)
            ),
            data=json.dumps(payload, sort_keys=True),
        )


class ClientRole(KeycloakAdminEntity):
    _paths: Dict[str, str] = {
        "single": "/auth/admin/realms/{realm}/clients/{id}/roles/{role_name}"
    }

    def __init__(
        self, realm_name: str, client_id: str, role_name: str, *args: Any, **kwargs: Any
    ):
        super().__init__(
            url=self.get_path(
                "single", realm=realm_name, id=client_id, role_name=role_name
            ),
            *args,
            **kwargs
        )
