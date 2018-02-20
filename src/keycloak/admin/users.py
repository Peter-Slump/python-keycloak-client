import json

from keycloak.admin import KeycloakAdminBase


class Users(KeycloakAdminBase):

    _paths = {
        'collection': '/auth/admin/realms/{realm}/users'
    }

    _realm_name = None

    def __init__(self, realm_name, *args, **kwargs):
        self._realm_name = realm_name
        super(Users, self).__init__(*args, **kwargs)

    def create(self, username, credentials=None, first_name=None,
               last_name=None, email=None, enabled=None):

        payload = {
            'username': username,
        }

        if credentials is not None:
            payload['credentials'] = [credentials]

        if first_name is not None:
            payload['firstName'] = first_name

        if last_name is not None:
            payload['lastName'] = last_name

        if email is not None:
            payload['email'] = email

        if enabled is not None:
            payload['enabled'] = enabled

        self._client.post(
            url=self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            ),
            data=json.dumps(payload)
        )
