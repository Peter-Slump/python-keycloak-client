from unittest import TestCase

import mock

from keycloak.admin import KeycloakAdmin
from keycloak.realm import KeycloakRealm


class KeycloakAdminGroupsTestCase(TestCase):

    def setUp(self):
        self.realm = mock.MagicMock(spec_set=KeycloakRealm)
        self.admin = KeycloakAdmin(realm=self.realm)
        self.admin.set_token('some-token')

    def test_create(self):
        self.admin.realms.by_name('realm-name').groups.create("group-name")
        self.realm.client.get_full_url.assert_called_once_with(
            '/admin/realms/realm-name/groups'
        )
        self.realm.client.post.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data='{"name": "group-name"}',
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_get_all(self):
        self.admin.realms.by_name('realm-name').groups.all()
        self.realm.client.get_full_url.assert_called_once_with(
            '/admin/realms/realm-name/groups'
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )
