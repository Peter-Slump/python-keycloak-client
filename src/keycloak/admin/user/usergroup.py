import json
from typing import Dict, Any

from .. import KeycloakAdminBase
from keycloak.client import JSONType


class UserGroups(KeycloakAdminBase):
    _BASE: str = "/auth/admin/realms/{realm}/users/{user_id}"
    _paths: Dict[str, str] = {
        "collection": _BASE + "/groups",
        "single": _BASE + "/groups/{group_id}",
    }

    def __init__(self, realm_name: str, user_id: str, *args: Any, **kwargs: Any):
        self._realm_name: str = realm_name
        self._user_id: str = user_id
        super(UserGroups, self).__init__(*args, **kwargs)

    def all(self) -> JSONType:
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    "collection", realm=self._realm_name, user_id=self._user_id
                )
            )
        )

    def add(self, group_id: str) -> JSONType:
        return self._client.put(
            url=self._client.get_full_url(
                self.get_path(
                    "single",
                    realm=self._realm_name,
                    user_id=self._user_id,
                    group_id=group_id,
                )
            ),
            data=json.dumps(
                {
                    "realm": self._realm_name,
                    "userId": self._user_id,
                    "groupId": group_id,
                }
            ),
        )

    def delete(self, group_id: str) -> JSONType:
        return self._client.delete(
            url=self._client.get_full_url(
                self.get_path(
                    "single",
                    realm=self._realm_name,
                    user_id=self._user_id,
                    group_id=group_id,
                )
            )
        )
