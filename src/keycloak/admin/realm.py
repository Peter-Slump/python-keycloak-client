import json

from keycloak.admin import KeycloakAdminBase, KeycloakAdminEntity

__all__ = ("Realm", "Realms")


class Realms(KeycloakAdminBase):
    _paths = {"collection": "/auth/admin/realms"}

    def __init__(self, *args, **kwargs):
        super(Realms, self).__init__(*args, **kwargs)

    def by_name(self, name):
        return Realm(name=name, client=self._client)

    def all(self):
        return self._client.get(self._client.get_full_url(self.get_path("collection")))

    def create(self, name, **kwargs):
        payload = {"realm": name, **kwargs}
        self._client.post(
            self._client.get_full_url(self.get_path("collection")), json.dumps(payload)
        )
        return Realm(name=name, client=self._client)


class Realm(KeycloakAdminEntity):
    _name = None
    _paths = {"single": "/auth/admin/realms/{realm}"}

    def __init__(self, name, client):
        self._name = name
        super(Realm, self).__init__(
            url=self.get_path("single", realm=name), client=client
        )

    @property
    def clients(self):
        from keycloak.admin.clients import Clients

        return Clients(realm_name=self._name, client=self._client)

    @property
    def users(self):
        from keycloak.admin.users import Users

        return Users(realm_name=self._name, client=self._client)

    @property
    def groups(self):
        from keycloak.admin.groups import Groups

        return Groups(realm_name=self._name, client=self._client)
