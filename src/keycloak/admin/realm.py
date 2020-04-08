import json
from typing import Dict, Any

from . import KeycloakAdminBase, KeycloakAdminEntity
from .clients import Clients
from .groups import Groups
from .users import Users

from keycloak.client import JSONType

__all__ = ("Realm", "Realms")


class Realms(KeycloakAdminBase):
    _paths: Dict[str, str] = {"collection": "/auth/admin/realms"}

    def by_name(self, name: str) -> "Realm":
        return Realm(name=name, client=self._client)

    def all(self) -> JSONType:
        return self._client.get(self._client.get_full_url(self.get_path("collection")))

    def create(self, name: str, **kwargs: Any) -> "Realm":
        payload = {"realm": name, **kwargs}
        self._client.post(
            self._client.get_full_url(self.get_path("collection")), json.dumps(payload)
        )
        return Realm(name=name, client=self._client)


class Realm(KeycloakAdminEntity):

    _paths: Dict[str, str] = {"single": "/auth/admin/realms/{realm}"}

    def __init__(self, name: str, *args: Any, **kwargs: Any):
        self._name: str = name
        super().__init__(url=self.get_path("single", realm=name), *args, **kwargs)

    @property
    def clients(self) -> Clients:
        return Clients(realm_name=self._name, client=self._client)

    @property
    def users(self) -> Users:
        return Users(realm_name=self._name, client=self._client)

    @property
    def groups(self) -> Groups:
        return Groups(realm_name=self._name, client=self._client)
