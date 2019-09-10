import json

from keycloak.admin import KeycloakAdminBase, KeycloakAdminEntity

__all__ = ('Client', 'Clients',)


class Clients(KeycloakAdminBase):
    _realm_name = None
    _paths = {
        'collection': '/auth/admin/realms/{realm}/clients'
    }

    def __init__(self, realm_name, *args, **kwargs):
        self._realm_name = realm_name
        super(Clients, self).__init__(*args, **kwargs)

    def all(self):
        return self._client.get(
            self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            )
        )

    def by_id(self, id):
        return Client(client=self._client, realm_name=self._realm_name, id=id)

    def by_client_id(self, client_id):
        id = next(iter([client["id"] for client in self.all() if client["clientId"] == client_id]), None)
        if id is None:
            return None
        return Client(client=self._client, realm_name=self._realm_name, id=id)

    def create(self, id, **kwargs):
        payload = {
            "id": id,
            **kwargs
        }
        self._client.post(
            self._client.get_full_url(
                self.get_path("collection", realm=self._realm_name)
            ),
            json.dumps(payload)
        )
        return Client(realm_name=self._realm_name, id=id, client=self._client)


class Client(KeycloakAdminEntity):
    _id = None
    _realm_name = None
    _BASE = '/auth/admin/realms/{realm}/clients/{id}'
    _paths = {
        'single': _BASE,
        'service_account': _BASE + '/service-account-user',
        'secret': _BASE + '/client-secret'
    }

    def __init__(self, realm_name, id, client):
        self._id = id
        self._realm_name = realm_name
        self._info = None
        super(Client, self).__init__(url=self.get_path("single", realm=realm_name, id=id),
                                     client=client)

    @property
    def roles(self):
        from keycloak.admin.clientroles import ClientRoles
        return ClientRoles(client=self._client, client_id=self._id,
                           realm_name=self._realm_name)

    @property
    def service_account_user(self):
        from keycloak.admin.users import User
        user = self._client.get(
            self._client.get_full_url(
                self.get_path('service_account', realm=self._realm_name, id=self._id)
            )
        )
        return User(user_id=user["id"], realm_name=self._realm_name, client=self._client)

    @property
    def secret(self):
        return self._client.get(
            self._client.get_full_url(
                self.get_path('secret', realm=self._realm_name, id=self._id)
            )
        )
