from unittest import TestCase

import mock

from keycloak.admin import KeycloakAdmin
from keycloak.realm import KeycloakRealm


class KeycloakAdminClientRolesTestCase(TestCase):

    def setUp(self):
        self.realm = mock.MagicMock(spec_set=KeycloakRealm)
        self.admin = KeycloakAdmin(realm=self.realm)
        self.admin.set_token('some-token')

    def test_create(self):
        self.admin.realms.by_name('realm-name').clients.by_id('#123').roles. \
            create(
            name='my-role-name',
            description='my-description',
            id='my-id',
            client_role='my-client-role',
            composite=False,
            composites='my-composites',
            container_id='my-container-id',
            scope_param_required=True
        )
        self.realm.client.get_full_url.assert_called_once_with(
            '/admin/realms/realm-name/clients/#123/roles'
        )
        self.realm.client.post.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data='{'
                 '"clientRole": "my-client-role", '
                 '"composite": false, '
                 '"composites": "my-composites", '
                 '"containerId": "my-container-id", '
                 '"description": "my-description", '
                 '"id": "my-id", '
                 '"name": "my-role-name", '
                 '"scopeParamRequired": true'
                 '}',
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_update(self):
        self.admin.realms.by_name('realm-name').clients.by_id(
            '#123').roles.by_name('role-name').update(
            name='my-role-name',
            description='my-description',
            id='my-id',
            client_role='my-client-role',
            composite=False,
            composites='my-composites',
            container_id='my-container-id',
            scope_param_required=True
        )
        self.realm.client.get_full_url.assert_called_once_with(
            '/admin/realms/realm-name/clients/#123/roles/role-name'
        )
        self.realm.client.put.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data='{'
                 '"clientRole": "my-client-role", '
                 '"composite": false, '
                 '"composites": "my-composites", '
                 '"containerId": "my-container-id", '
                 '"description": "my-description", '
                 '"id": "my-id", '
                 '"name": "my-role-name", '
                 '"scopeParamRequired": true'
                 '}',
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )
