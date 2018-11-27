import asynctest

try:
    import aiohttp  # noqa: F401
except ImportError:
    aiohttp = None
else:
    from keycloak.admin import KeycloakAdmin
    from keycloak.aio.authz import KeycloakAuthz
    from keycloak.aio.client import KeycloakClient
    from keycloak.aio.openid_connect import KeycloakOpenidConnect
    from keycloak.aio.uma import KeycloakUMA
    from keycloak.aio.realm import KeycloakRealm


async def wraps_awaitable(return_value):
    return return_value


@asynctest.skipIf(aiohttp is None, 'aiohttp is not installed')
class KeycloakRealmTestCase(asynctest.TestCase):

    async def setUp(self):
        self.mocked_client_patcher = asynctest.patch(
            'keycloak.aio.realm.KeycloakClient',
            autospec=True,
        )

        self.mocked_client = self.mocked_client_patcher.start()

        self.mocked_client.return_value = asynctest.CoroutineMock(
            return_value=wraps_awaitable(
                return_value=self.mocked_client.return_value
            )
        )()

        self.realm = await KeycloakRealm(
            'https://example.com',
            'some-realm',
            headers={'some': 'header'},
            loop=self.loop,
        )
        self.addCleanup(self.mocked_client_patcher.stop)

    def test_instance(self):
        """
        Case: Realm is instantiated
        Expected: Name and server_url are exposed
        """
        self.assertEqual(self.realm.realm_name, 'some-realm')
        self.assertEqual(self.realm.server_url, 'https://example.com')

    async def test_client(self):
        """
        Case: Client get requested
        Expected: Client get returned and the second time the same get returned
        """

        async with self.realm:
            client = self.realm.client

            self.assertIsInstance(client, KeycloakClient)

            self.assertEqual(client, self.realm.client)

            self.mocked_client.assert_called_once_with(
                server_url='https://example.com',
                headers={'some': 'header'},
                loop=self.loop
            )

    async def test_openid_connect(self):
        """
        Case: OpenID client get requested
        Expected: OpenID client get returned
        """
        with asynctest.patch(target='keycloak.aio.realm.KeycloakOpenidConnect',
                             autospec=True) as mocked_openid_client:
            async with self.realm:
                openid_client = self.realm.open_id_connect(
                    client_id='client-id',
                    client_secret='client-secret'
                )

                self.assertIsInstance(openid_client, KeycloakOpenidConnect)
                self.assertEqual(
                    openid_client,
                    mocked_openid_client.return_value
                )
                mocked_openid_client.assert_called_once_with(
                    realm=self.realm,
                    client_id='client-id',
                    client_secret='client-secret'
                )

    async def test_admin(self):
        """
        Case: Admin client get requested
        Expected: Admin client get returned
        """
        with asynctest.patch('keycloak.realm.KeycloakAdmin',
                             autospec=True) as mocked_admin_client:
            async with self.realm:
                admin_client = self.realm.admin
                self.assertIsInstance(admin_client, KeycloakAdmin)
                mocked_admin_client.assert_called_once_with(realm=self.realm)

    async def test_authz(self):
        """
        Case: Authz client get requested
        Expected: Authz client get returned
        """
        with asynctest.patch('keycloak.aio.realm.KeycloakAuthz',
                             autospec=True) as mocked_authz_client:
            async with self.realm:
                authz_client = self.realm.authz(client_id='client-id')

                self.assertIsInstance(authz_client, KeycloakAuthz)
                mocked_authz_client.assert_called_once_with(
                    realm=self.realm,
                    client_id='client-id'
                )

    async def test_uma(self):
        """
        Case: UMA client get requested
        Expected: UMA client get returned
        """
        with asynctest.patch('keycloak.aio.realm.KeycloakUMA',
                             autospec=True) as mocked_uma_client:
            async with self.realm:
                uma_client = self.realm.uma()

                self.assertIsInstance(uma_client, KeycloakUMA)
                mocked_uma_client.assert_called_once_with(realm=self.realm)
