from unittest import TestCase

import mock

from keycloak.admin import KeycloakAdmin
from keycloak.realm import KeycloakRealm


class KeycloakAdminUsersTestCase(TestCase):

    def setUp(self):
        self.realm = mock.MagicMock(spec_set=KeycloakRealm)
        self.admin = KeycloakAdmin(realm=self.realm)
        self.admin.set_token('some-token')

    def test_create(self):
        self.admin.realms.by_name('realm-name').users.create(
            username='my-username',
            credentials={'some': 'value'},
            first_name='my-first-name',
            last_name='my-last-name',
            email='my-email',
            enabled=True
        )
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/users'
        )
        self.realm.client.post.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data='{"username": "my-username", '
                 '"credentials": [{"some": "value"}], '
                 '"firstName": "my-first-name", '
                 '"lastName": "my-last-name", '
                 '"email": "my-email", '
                 '"enabled": true}',
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_get_collection(self):
        self.admin.realms.by_name('realm-name').users.all()
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/users'
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_get_single(self):
        self.admin.realms.by_name('realm-name').users.by_id('an-id').get()
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/users/an-id'
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )
