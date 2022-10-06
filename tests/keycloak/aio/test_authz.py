import asynctest

try:
    import aiohttp  # noqa: F401
except ImportError:
    aiohttp = None
else:
    from keycloak.aio.authz import KeycloakAuthz
    from keycloak.aio.client import KeycloakClient
    from keycloak.aio.realm import KeycloakRealm


@asynctest.skipIf(aiohttp is None, 'aiohttp is not installed')
class KeycloakAuthzTestCase(asynctest.TestCase):
    async def setUp(self):
        self.realm = asynctest.MagicMock(spec_set=KeycloakRealm)
        self.realm.client = asynctest.MagicMock(spec_set=KeycloakClient)
        self.realm.client.get = asynctest.CoroutineMock()
        self.realm.realm_name = 'realm-name'
        self.client_id = 'client-id'
        self.authz = await KeycloakAuthz(realm=self.realm,
                                         client_id=self.client_id)

    async def tearDown(self):
        await self.realm.close()

    def test_well_known_loaded(self):
        assert self.realm.client.get_full_url.call_count == 1
        assert self.realm.client.get.await_count == 1

    async def test_entitlement(self):
        result = await self.authz.entitlement(token='some-token')

        self.realm.client.get_full_url.assert_any_call(
            'realms/realm-name/authz/entitlement/client-id'
        )
        self.realm.client.get.assert_any_await(
            self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token'
            }
        )
        self.assertEqual(result, self.realm.client.get.return_value)
