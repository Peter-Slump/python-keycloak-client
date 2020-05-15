import json
from typing import Any, Dict, List

from keycloak.admin import KeycloakAdminBase
from keycloak.client import JSONType

__all__ = ("UserRoleMappings", "UserRoleMappingsRealm")


class UserRoleMappings(KeycloakAdminBase):
    def __init__(self, realm_name: str, user_id: str, *args: Any, **kwargs: Any):
        self._realm_name: str = realm_name
        self._user_id: str = user_id
        super().__init__(*args, **kwargs)

    @property
    def realm(self) -> "UserRoleMappingsRealm":
        return UserRoleMappingsRealm(
            realm_name=self._realm_name, user_id=self._user_id, client=self._client
        )

    def client(self, client_id: str):
        return UserRoleMappingsClient(
            realm_name=self._realm_name,
            user_id=self._user_id,
            client_id=client_id,
            client=self._client,
        )


class UserRoleMappingsRealm(KeycloakAdminBase):
    _paths: Dict[str, str] = {
        "available": (
            "/auth/admin/realms/{realm}/users/{id}/role-mappings/realm/available"
        ),
        "single": "/auth/admin/realms/{realm}/users/{id}/role-mappings/realm",
    }

    def __init__(self, realm_name: str, user_id: str, *args: Any, **kwargs: Any):
        self._realm_name: str = realm_name
        self._user_id: str = user_id
        super().__init__(*args, **kwargs)

    def available(self) -> JSONType:
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path("available", realm=self._realm_name, id=self._user_id)
            )
        )

    def add(self, roles: List[Any]) -> JSONType:
        """
        :param roles: _rolerepresentation array keycloak api
        """
        return self._client.post(
            url=self._client.get_full_url(
                self.get_path("single", realm=self._realm_name, id=self._user_id)
            ),
            data=json.dumps(roles, sort_keys=True),
        )

    def get(self) -> JSONType:
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path("single", realm=self._realm_name, id=self._user_id)
            )
        )

    def delete(self, roles: List[Any]) -> JSONType:
        """
        :param roles: _rolerepresentation array keycloak api
        """
        return self._client.delete(
            url=self._client.get_full_url(
                self.get_path("single", realm=self._realm_name, id=self._user_id)
            ),
            data=json.dumps(roles, sort_keys=True),
        )


class UserRoleMappingsClient(KeycloakAdminBase):
    _BASE: str = (
        "/auth/admin/realms/{realm}/users/{id}/role-mappings/clients/{client_id}"
    )
    _paths: Dict[str, str] = {"available": _BASE + "/available", "single": _BASE}

    def __init__(
        self, realm_name: str, user_id: str, client_id: str, *args: Any, **kwargs: Any
    ):
        self._realm_name: str = realm_name
        self._user_id: str = user_id
        self._client_id: str = client_id
        super().__init__(*args, **kwargs)

    def available(self) -> JSONType:
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    "available",
                    realm=self._realm_name,
                    id=self._user_id,
                    client_id=self._client_id,
                )
            )
        )

    def add(self, roles: List[Any]) -> JSONType:
        """
        roles -- List of roles to add
        """
        return self._client.post(
            url=self._client.get_full_url(
                self.get_path(
                    "single",
                    realm=self._realm_name,
                    id=self._user_id,
                    client_id=self._client_id,
                )
            ),
            data=json.dumps(roles, sort_keys=True),
        )

    def get(self) -> JSONType:
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    "single",
                    realm=self._realm_name,
                    id=self._user_id,
                    client_id=self._client_id,
                )
            )
        )

    def delete(self, roles: List[Any]) -> JSONType:
        """
        :param roles: _rolerepresentation array keycloak api
        """
        return self._client.delete(
            url=self._client.get_full_url(
                self.get_path(
                    "single",
                    realm=self._realm_name,
                    id=self._user_id,
                    client_id=self._client_id,
                )
            ),
            data=json.dumps(roles, sort_keys=True),
        )
