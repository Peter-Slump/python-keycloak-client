import json
from typing import Any, Dict

from keycloak.client import JSONType

from . import KeycloakAdminBase

__all__ = ("Groups",)


class Groups(KeycloakAdminBase):
    _paths: Dict[str, str] = {"collection": "/auth/admin/realms/{realm}/groups"}

    def __init__(self, realm_name: str, *args: Any, **kwargs: Any):
        self._realm_name: str = realm_name
        super().__init__(*args, **kwargs)

    def all(self) -> JSONType:
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path("collection", realm=self._realm_name)
            )
        )

    def create(self, name: str) -> JSONType:
        return self._client.post(
            url=self._client.get_full_url(
                self.get_path("collection", realm=self._realm_name)
            ),
            data=json.dumps({"name": name}),
        )
