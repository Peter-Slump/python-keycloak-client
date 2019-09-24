from unittest import TestCase

import mock

from keycloak.admin import KeycloakAdmin
from keycloak.realm import KeycloakRealm


class KeycloakAdminUserRolesTestCase(TestCase):
    def setUp(self):
        self.realm = mock.MagicMock(spec_set=KeycloakRealm)
        self.admin = KeycloakAdmin(realm=self.realm)
        self.admin.set_token("some-token")

    def test_add_role(self):
        role_representations = [
            {
                "id": "00000000-0000-0000-0000-000000000000",
                "name": "Admin",
                "description": "${Admin}",
                "composite": True,
                "clientRole": False,
                "containerId": "master",
            }
        ]
        self.admin.realms.by_name("realm-name").users.by_id(
            "user-id"
        ).role_mappings.realm.add(role_representations)
        self.realm.client.get_full_url.assert_called_once_with(
            "/auth/admin/realms/realm-name/users/user-id" + "/role-mappings/realm"
        )
        self.realm.client.post.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data="["
            "{"
            '"clientRole": false, '
            '"composite": true, '
            '"containerId": "master", '
            '"description": "${Admin}", '
            '"id": "00000000-0000-0000-0000-000000000000", '
            '"name": "Admin"'
            "}"
            "]",
            headers={
                "Authorization": "Bearer some-token",
                "Content-Type": "application/json",
            },
        )

    def test_get_available_realm_role(self):
        self.admin.realms.by_name("realm-name").users.by_id(
            "user-id"
        ).role_mappings.realm.available()
        self.realm.client.get_full_url.assert_called_once_with(
            "/auth/admin/realms/realm-name/users/user-id"
            + "/role-mappings/realm/available"
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                "Authorization": "Bearer some-token",
                "Content-Type": "application/json",
            },
        )

    def test_get_realm_role(self):
        self.admin.realms.by_name("realm-name").users.by_id(
            "user-id"
        ).role_mappings.realm.get()
        self.realm.client.get_full_url.assert_called_once_with(
            "/auth/admin/realms/realm-name/users/user-id" + "/role-mappings/realm"
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                "Authorization": "Bearer some-token",
                "Content-Type": "application/json",
            },
        )

    def test_delete_role(self):
        role_representations = [
            {
                "id": "00000000-0000-0000-0000-000000000000",
                "name": "Admin",
                "description": "${Admin}",
                "composite": True,
                "clientRole": False,
                "containerId": "master",
            }
        ]
        self.admin.realms.by_name("realm-name").users.by_id(
            "user-id"
        ).role_mappings.realm.delete(role_representations)
        self.realm.client.get_full_url.assert_called_once_with(
            "/auth/admin/realms/realm-name/users/user-id" + "/role-mappings/realm"
        )
        self.realm.client.delete.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data="["
            "{"
            '"clientRole": false, '
            '"composite": true, '
            '"containerId": "master", '
            '"description": "${Admin}", '
            '"id": "00000000-0000-0000-0000-000000000000", '
            '"name": "Admin"'
            "}"
            "]",
            headers={
                "Authorization": "Bearer some-token",
                "Content-Type": "application/json",
            },
        )
