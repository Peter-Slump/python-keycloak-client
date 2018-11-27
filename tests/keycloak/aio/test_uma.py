import asynctest
try:
    import aiohttp  # noqa: F401
except ImportError:
    aiohttp = None
else:
    from keycloak.aio.uma import KeycloakUMA
    from keycloak.aio.realm import KeycloakRealm
    from keycloak.aio.well_known import KeycloakWellKnown


@asynctest.skipIf(aiohttp is None, 'aiohttp is not installed')
class KeycloakOpenidConnectTestCase(asynctest.TestCase):
    async def setUp(self):
        self.realm = asynctest.MagicMock(spec_set=KeycloakRealm)
        self.realm.client.get = asynctest.CoroutineMock()
        self.realm.client.post = asynctest.CoroutineMock()
        self.realm.client.put = asynctest.CoroutineMock()
        self.realm.client.delete = asynctest.CoroutineMock()

        self.uma_client = await KeycloakUMA(realm=self.realm)
        self.uma_client.well_known.contents = {
            'resource_registration_endpoint': 'https://resource_registration',
            'permission_endpoint': 'https://permission',
            'policy_endpoint': 'https://policy',
        }

    async def tearDown(self):
        await self.uma_client.close()

    def test_well_known(self):
        """
        Case: .well-known is requested
        Expected: it's returned and the second time the same is returned
        """
        well_known = self.uma_client.well_known

        self.assertIsInstance(well_known, KeycloakWellKnown)
        self.assertEqual(well_known, self.uma_client.well_known)

    async def test_resource_set_create(self):
        result = await self.uma_client.resource_set_create(
            token='test-token',
            name='test-name',
            optional_param='test-optional-param'
        )

        self.realm.client.post.assert_awaited_once_with(
            'https://resource_registration',
            data=self.uma_client._get_data(
                name='test-name',
                optional_param='test-optional-param'
            ),
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.post.return_value)

    async def test_resource_set_update(self):
        result = await self.uma_client.resource_set_update(
            token='test-token',
            id='test-id',
            name='test-name',
            optional_param='test-optional-param'
        )

        self.realm.client.put.assert_awaited_once_with(
            'https://resource_registration/test-id',
            data=self.uma_client._get_data(
                name='test-name',
                optional_param='test-optional-param'
            ),
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.put.return_value)

    async def test_resource_set_read(self):
        result = await self.uma_client.resource_set_read(
            token='test-token',
            id='test-id',
        )

        self.realm.client.get.assert_called_with(
            'https://resource_registration/test-id',
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.get.return_value)

    async def test_resource_set_delete(self):
        result = await self.uma_client.resource_set_delete(
            token='test-token',
            id='test-id',
        )

        self.realm.client.delete.assert_awaited_once_with(
            'https://resource_registration/test-id',
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.delete.return_value)

    async def test_resource_set_list(self):
        result = await self.uma_client.resource_set_list(
            token='test-token',
            name='test-name',
            owner='test-owner'
        )

        self.realm.client.get.assert_called_with(
            'https://resource_registration',
            name='test-name',
            owner='test-owner',
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.get.return_value)

    async def test_resource_create_ticket(self):
        result = await self.uma_client.resource_create_ticket(
            token='test-token',
            id='test-id',
            scopes=['test-scope'],
            optional_param='test-optional-param'
        )

        self.realm.client.post.assert_awaited_once_with(
            'https://permission',
            data=self.uma_client._dumps([
                dict(
                    resource_id='test-id',
                    resource_scopes=['test-scope'],
                    optional_param='test-optional-param'
                )
            ]),
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.post.return_value)

    async def test_resource_associate_permission(self):
        result = await self.uma_client.resource_associate_permission(
            token='test-token',
            id='test-id',
            name='test-name',
            scopes=['test-scope'],
            optional_param='test-optional-param'
        )

        self.realm.client.post.assert_awaited_once_with(
            'https://policy/test-id',
            data=self.uma_client._get_data(
                name='test-name',
                scopes=['test-scope'],
                optional_param='test-optional-param'
            ),
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.post.return_value)

    async def test_permission_update(self):
        result = await self.uma_client.permission_update(
            token='test-token',
            id='test-id',
            optional_param='test-optional-param'
        )

        self.realm.client.put.assert_awaited_once_with(
            'https://policy/test-id',
            data='{"optional_param": "test-optional-param"}',
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.put.return_value)

    async def test_permission_delete(self):
        result = await self.uma_client.permission_delete(
            token='test-token',
            id='test-id',
        )

        self.realm.client.delete.assert_awaited_once_with(
            'https://policy/test-id',
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.delete.return_value)

    async def test_permission_list(self):
        result = await self.uma_client.permission_list(
            token='test-token',
            name='test-name',
            resource='test-resource'
        )

        self.realm.client.get.assert_called_with(
            'https://policy',
            name='test-name',
            resource='test-resource',
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.get.return_value)
