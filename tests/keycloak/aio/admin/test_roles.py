import asynctest

try:
    import aiohttp
except ImportError:
    aiohttp = None
else:
    from keycloak.admin import KeycloakAdmin
    from keycloak.aio.realm import KeycloakRealm
    from keycloak.client import KeycloakClient


@asynctest.skipIf(aiohttp is None, "aiohttp is not installed")
class KeycloakAdminRolesTestCase(asynctest.TestCase):
    def setUp(self):
        self.realm = asynctest.MagicMock(spec_set=KeycloakRealm)
        self.realm.client = asynctest.MagicMock(spec_set=KeycloakClient)()
        self.realm.client.get = asynctest.CoroutineMock()
        self.realm.client.post = asynctest.CoroutineMock()
        self.realm.client.put = asynctest.CoroutineMock()
        self.realm.client.delete = asynctest.CoroutineMock()
        self.realm.realm_name = "realm-name"
        self.client_id = "client-id"
        self.admin = KeycloakAdmin(realm=self.realm)
        self.admin.set_token("some-token")

    async def tearDown(self):
        await self.realm.close()

    async def test_create(self):
        await self.admin.realms.by_name("realm-name").clients.by_id(
            "#123"
        ).roles.create(
            name="my-role-name",
            description="my-description",
            id="my-id",
            client_role="my-client-role",
            composite=False,
            composites="my-composites",
            container_id="my-container-id",
            scope_param_required=True,
        )

        self.realm.client.get_full_url.assert_called_once_with(
            "/auth/admin/realms/realm-name/clients/#123/roles"
        )
        self.realm.client.post.assert_awaited_once_with(
            url=self.realm.client.get_full_url.return_value,
            data='{"clientRole": "my-client-role", '
            '"composite": false, '
            '"composites": "my-composites", '
            '"containerId": "my-container-id", '
            '"description": "my-description", '
            '"id": "my-id", '
            '"name": "my-role-name", '
            '"scopeParamRequired": true}',
            headers={
                "Authorization": "Bearer some-token",
                "Content-Type": "application/json",
            },
        )

    async def test_update(self):
        await self.admin.realms.by_name("realm-name").clients.by_id(
            "#123"
        ).roles.by_name("role-name").update(
            name="my-role-name",
            description="my-description",
            id="my-id",
            client_role="my-client-role",
            composite=False,
            composites="my-composites",
            container_id="my-container-id",
            scope_param_required=True,
        )
        self.realm.client.get_full_url.assert_called_once_with(
            "/auth/admin/realms/realm-name/clients/#123/roles/role-name"
        )
        self.realm.client.put.assert_awaited_once_with(
            url=self.realm.client.get_full_url.return_value,
            data='{"clientRole": "my-client-role", '
            '"composite": false, '
            '"composites": "my-composites", '
            '"containerId": "my-container-id", '
            '"description": "my-description", '
            '"id": "my-id", "name": '
            '"my-role-name", '
            '"scopeParamRequired": true}',
            headers={
                "Authorization": "Bearer some-token",
                "Content-Type": "application/json",
            },
        )
