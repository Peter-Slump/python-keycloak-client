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
            credentials=[{'some': 'value'}],
            first_name='my-first-name',
            last_name='my-last-name',
            email='my-email',
            enabled=True
        )
        self.realm.client.get_full_url.assert_called_once_with(
            '/admin/realms/realm-name/users'
        )
        self.realm.client.post.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data='{'
                 '"credentials": ['
                 '{'
                 '"some": "value"'
                 '}'
                 '], '
                 '"email": "my-email", '
                 '"enabled": true, '
                 '"firstName": "my-first-name", '
                 '"lastName": "my-last-name", '
                 '"username": "my-username"'
                 '}',
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_get_collection(self):
        self.admin.realms.by_name('realm-name').users.all()
        self.realm.client.get_full_url.assert_called_once_with(
            '/admin/realms/realm-name/users'
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
            '/admin/realms/realm-name/users/an-id'
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_get_single_user(self):
        self.admin.realms.by_name('realm-name').users.by_id('an-id').user
        self.realm.client.get_full_url.assert_called_once_with(
            '/admin/realms/realm-name/users/an-id'
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    @mock.patch('keycloak.admin.users.User.user', {"id": "user-id"})
    def test_update(self):
        user = self.admin.realms.by_name('realm-name').users.by_id("user-id")
        user.update(
            credentials=[{'some': 'value'}],
            first_name='my-first-name',
            last_name='my-last-name',
            email='my-email',
            enabled=True
        )
        self.realm.client.get_full_url.assert_called_with(
            '/admin/realms/realm-name/users/user-id'
        )
        self.realm.client.put.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data='{'
                 '"credentials": ['
                 '{'
                 '"some": "value"'
                 '}'
                 '], '
                 '"email": "my-email", '
                 '"enabled": true, '
                 '"firstName": "my-first-name", '
                 '"id": "user-id", '
                 '"lastName": "my-last-name"'
                 '}',
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    @mock.patch('keycloak.admin.users.User.user', {"id": "user-id"})
    def test_delete(self):
        user = self.admin.realms.by_name('realm-name').users.by_id("user-id")
        user.delete()
        self.realm.client.get_full_url.assert_called_with(
            '/admin/realms/realm-name/users/user-id'
        )
        self.realm.client.delete.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    @mock.patch('keycloak.admin.users.User.user', {"id": "user-id"})
    def test_delete_group(self):
        user = self.admin.realms.by_name('realm-name').users.by_id("user-id")
        user.groups.delete('group-id')
        self.realm.client.get_full_url.assert_called_with(
            '/admin/realms/realm-name/users/user-id/groups/group-id'
        )
        self.realm.client.delete.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    @mock.patch('keycloak.admin.users.User.user', {"id": "user-id"})
    def test_reset_password(self):
        user = self.admin.realms.by_name('realm-name').users.by_id("user-id")
        user.reset_password("password", True)
        self.realm.client.get_full_url.assert_called_with(
            '/admin/realms/realm-name/users/user-id/reset-password'
        )
        self.realm.client.put.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data='{"temporary": true, '
                 '"type": "password", '
                 '"value": "password"}',
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    @mock.patch('keycloak.admin.users.User.user', {"id": "user-id"})
    def test_logout_user(self):
        user = self.admin.realms.by_name('realm-name').users.by_id("user-id")
        user.logout()
        self.realm.client.get_full_url.assert_called_with(
            '/admin/realms/realm-name/users/user-id/logout'
        )
        self.realm.client.post.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data=None,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )
