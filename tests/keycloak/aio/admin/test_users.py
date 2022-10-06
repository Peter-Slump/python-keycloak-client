import asynctest

try:
    import aiohttp
except ImportError:
    aiohttp = None
else:
    from keycloak.admin import KeycloakAdmin
    from keycloak.client import KeycloakClient
    from keycloak.realm import KeycloakRealm


@asynctest.skipIf(aiohttp is None, 'aiohttp is not installed')
class KeycloakAdminUsersTestCase(asynctest.TestCase):

    def setUp(self):
        self.realm = asynctest.MagicMock(spec_set=KeycloakRealm)
        self.realm.client = asynctest.MagicMock(spec_set=KeycloakClient)()
        self.realm.client.get = asynctest.CoroutineMock()
        self.realm.client.post = asynctest.CoroutineMock()
        self.realm.client.put = asynctest.CoroutineMock()
        self.realm.client.delete = asynctest.CoroutineMock()
        self.admin = KeycloakAdmin(realm=self.realm)
        self.admin.set_token('some-token')

    async def test_create(self):
        await self.admin.realms.by_name('realm-name').users.create(
            username='my-username',
            credentials={'some': 'value'},
            first_name='my-first-name',
            last_name='my-last-name',
            email='my-email',
            enabled=True
        )
        self.realm.client.get_full_url.assert_called_once_with(
            '/admin/realms/realm-name/users'
        )
        self.realm.client.post.assert_awaited_once_with(
            url=self.realm.client.get_full_url.return_value,
            data='{"credentials": {"some": "value"}, '
                 '"email": "my-email", '
                 '"enabled": true, '
                 '"firstName": "my-first-name", '
                 '"lastName": "my-last-name", '
                 '"username": "my-username"}',
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )
