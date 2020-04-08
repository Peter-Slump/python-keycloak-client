import json
from typing import Any, Dict, Optional, Union

from keycloak.client import JSONType

from . import KeycloakAdminBase, KeycloakAdminEntity
from .clientroles import ClientRoles
from .users import User

__all__ = ("Client", "Clients")


class Clients(KeycloakAdminBase):
    _paths: Dict[str, str] = {"collection": "/auth/admin/realms/{realm}/clients"}

    def __init__(self, realm_name: str, *args: Any, **kwargs: Any):
        self._realm_name: str = realm_name
        super().__init__(*args, **kwargs)

    def all(self) -> JSONType:
        return self._client.get(
            self._client.get_full_url(
                self.get_path("collection", realm=self._realm_name)
            )
        )

    def by_id(self, id: str) -> "Client":
        return Client(client=self._client, realm_name=self._realm_name, id=id)

    def by_client_id(self, client_id) -> Optional["Client"]:
        id: Union[str, None] = next(
            iter(
                [
                    client["id"]
                    for client in self.all()
                    if client["clientId"] == client_id
                ]
            ),
            None,
        )
        if id is None:
            return None
        return Client(client=self._client, realm_name=self._realm_name, id=id)

    def create(self, id: str, **kwargs: Any) -> "Client":
        payload = {"id": id, **kwargs}
        self._client.post(
            self._client.get_full_url(
                self.get_path("collection", realm=self._realm_name)
            ),
            json.dumps(payload),
        )
        return Client(realm_name=self._realm_name, id=id, client=self._client)


class Client(KeycloakAdminEntity):
    _BASE: str = "/auth/admin/realms/{realm}/clients/{id}"
    _paths: Dict[str, str] = {
        "single": _BASE,
        "service_account": _BASE + "/service-account-user",
        "secret": _BASE + "/client-secret",
    }

    def __init__(self, realm_name: str, id: str, *args: Any, **kwargs: Any):
        self._id: str = id
        self._realm_name: str = realm_name
        self._info = None
        super().__init__(
            url=self.get_path("single", realm=realm_name, id=id), *args, **kwargs
        )

    @property
    def roles(self) -> ClientRoles:
        return ClientRoles(
            client=self._client, client_id=self._id, realm_name=self._realm_name
        )

    @property
    def service_account_user(self) -> User:
        user = self._client.get(
            self._client.get_full_url(
                self.get_path("service_account", realm=self._realm_name, id=self._id)
            )
        )
        return User(
            user_id=user["id"], realm_name=self._realm_name, client=self._client
        )

    @property
    def secret(self) -> JSONType:
        return self._client.get(
            self._client.get_full_url(
                self.get_path("secret", realm=self._realm_name, id=self._id)
            )
        )
