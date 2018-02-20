from keycloak.admin import KeycloakAdminBase


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


class Client(KeycloakAdminBase):

    _id = None
    _realm_name = None

    def __init__(self, realm_name, id, *args, **kwargs):
        self._id = id
        self._realm_name = realm_name
        super(Client, self).__init__(*args, **kwargs)

    @property
    def roles(self):
        from keycloak.admin.roles import Roles
        return Roles(client=self._client, client_id=self._id,
                     realm_name=self._realm_name)
