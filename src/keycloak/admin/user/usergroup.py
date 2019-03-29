import json

from keycloak.admin import KeycloakAdminBase


class UserGroups(KeycloakAdminBase):
    _BASE = "/auth/admin/realms/{realm}/users/{user_id}"
    _paths = {
        'collection': _BASE + '/groups',
        'single': _BASE + '/groups/{group_id}'
    }

    def __init__(self, realm_name, user_id, *args, **kwargs):
        self._realm_name = realm_name
        self._user_id = user_id
        super(UserGroups, self).__init__(*args, **kwargs)

    def all(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    'collection',
                    realm=self._realm_name,
                    user_id=self._user_id
                )
            )
        )

    def add(self, group_id):
        return self._client.put(
            url=self._client.get_full_url(
                self.get_path(
                    'single',
                    realm=self._realm_name,
                    user_id=self._user_id,
                    group_id=group_id
                )
            ),
            data=json.dumps({
                "realm": self._realm_name,
                "userId": self._user_id,
                "groupId": group_id
            })
        )

    def delete(self, group_id):
        return self._client.delete(
            url=self._client.get_full_url(
                self.get_path(
                    'single',
                    realm=self._realm_name,
                    user_id=self._user_id,
                    group_id=group_id
                )
            )
        )
