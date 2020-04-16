import json
from collections import OrderedDict
from typing import Any, Dict, Optional

from keycloak.client import JSONType

from . import KeycloakAdminBase, KeycloakAdminEntity, to_camel_case
from .user.usergroup import UserGroups
from .user.userroles import UserRoleMappings

__all__ = ("Users", "User")

USER_KWARGS = [
    "email",
    "first_name",
    "last_name",
    "email_verified",
    "attributes",
    "realm_roles",
    "client_roles",
    "groups",
    "enabled",
    "credentials",
]


class Users(KeycloakAdminBase):
    _paths: Dict[str, str] = {"collection": "/auth/admin/realms/{realm}/users"}

    def __init__(self, realm_name: str, *args: Any, **kwargs: Any):
        self._realm_name: str = realm_name
        super().__init__(*args, **kwargs)

    def create(self, username: str, **kwargs: Any) -> JSONType:
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

        for key in USER_KWARGS:
            if key in kwargs:
                payload[to_camel_case(key)] = kwargs[key]

        return self._client.post(
            url=self._client.get_full_url(
                self.get_path("collection", realm=self._realm_name)
            ),
            data=json.dumps(payload, sort_keys=True),
        )

    def all(self) -> JSONType:
        """
        Return all registered users

        http://www.keycloak.org/docs-api/3.4/rest-api/index.html#_users_resource
        """
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path("collection", realm=self._realm_name)
            )
        )

    def by_username(self, username: str) -> "User":
        users = self._client.get(
            url=self._client.get_full_url(
                self.get_path("collection", realm=self._realm_name)
            ),
            username=username,
        )
        return User(
            realm_name=self._realm_name, user_id=users[0]["id"], client=self._client
        )

    def by_id(self, user_id: str) -> "User":
        return User(realm_name=self._realm_name, user_id=user_id, client=self._client)


class User(KeycloakAdminEntity):
    _BASE: str = "/auth/admin/realms/{realm}/users/{user_id}"
    _paths: Dict[str, str] = {
        "single": _BASE,
        "reset_password": _BASE + "/reset-password",
    }

    def __init__(self, realm_name: str, user_id: str, *args: Any, **kwargs: Any):
        self._realm_name: str = realm_name
        self._user_id: str = user_id
        kwargs["url"] = self.get_path("single", realm=realm_name, user_id=user_id)
        super().__init__(*args, **kwargs)

    @property
    def user(self) -> JSONType:
        return self.entity

    @property
    def role_mappings(self) -> UserRoleMappings:
        return UserRoleMappings(
            realm_name=self._realm_name, user_id=self._user_id, client=self._client
        )

    @property
    def groups(self) -> UserGroups:
        return UserGroups(
            realm_name=self._realm_name, user_id=self._user_id, client=self._client
        )

    def update(self, **kwargs: Any) -> JSONType:
        data = {**kwargs, "id": self._user_id}
        return super().update(**data)

    def reset_password(
        self, password: str, temporary: Optional[bool] = False
    ) -> JSONType:
        payload = {"type": "password", "value": password, "temporary": temporary}
        result = self._client.put(
            url=self._client.get_full_url(
                self.get_path(
                    "reset_password", realm=self._realm_name, user_id=self._user_id
                )
            ),
            data=json.dumps(payload, sort_keys=True),
        )
        return result
