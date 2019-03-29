import json

from keycloak.admin import KeycloakAdminBase

__all__ = ('Groups',)


class Groups(KeycloakAdminBase):
    _paths = {
        'collection': '/auth/admin/realms/{realm}/groups',
    }

    def __init__(self, realm_name, *args, **kwargs):
        self._realm_name = realm_name
        super(Groups, self).__init__(*args, **kwargs)

    def all(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    'collection',
                    realm=self._realm_name
                )
            ),
        )

    def create(self, name):
        return self._client.post(
            url=self._client.get_full_url(
                self.get_path(
                    'collection',
                    realm=self._realm_name
                )
            ),
            data=json.dumps({
                "name": name
            })
        )
