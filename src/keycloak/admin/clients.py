import json
from typing import Any, Dict, Optional, Union, List

from keycloak.admin import to_camel_case
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

    def all(self, **kwargs) -> JSONType:
        """
        :param client_id:
        """
        return self._client.get(
            self._client.get_full_url(
                self.get_path("collection", realm=self._realm_name)
            ),
            **{to_camel_case(key): value for key, value in kwargs.items()}
        )

    def by_id(self, id: str) -> "Client":
        return Client(client=self._client, realm_name=self._realm_name, id=id)

    def by_client_id(self, client_id) -> List[JSONType]:
        return self.all(client_id=client_id)

    def create(self, id: str, **kwargs: Any) -> JSONType:
        payload = {"id": id, **kwargs}
        return self._client.post(
            self._client.get_full_url(
                self.get_path("collection", realm=self._realm_name)
            ),
            json.dumps(payload),
        )


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
