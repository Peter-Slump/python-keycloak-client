from unittest import TestCase

import mock

from keycloak.realm import KeycloakRealm
from keycloak.uma1 import KeycloakUMA1
from keycloak.well_known import KeycloakWellKnown


class KeycloakUma1TestCase(TestCase):

    def setUp(self):
        self.realm = mock.MagicMock(spec_set=KeycloakRealm)
        self.uma_client = KeycloakUMA1(realm=self.realm)
        self.uma_client.well_known.contents = {
            'resource_set_registration_endpoint':
                'https://resource_registration',
        }

    def test_well_known(self):
        """
        Case: .well-known is requested
        Expected: it's returned and the second time the same is returned
        """
        well_known = self.uma_client.well_known

        self.assertIsInstance(well_known, KeycloakWellKnown)
        self.assertEqual(well_known, self.uma_client.well_known)

    def test_get_headers(self):
        result = self.uma_client.get_headers(token='test-token')
        self.assertEqual(result, {
            "Authorization": "Bearer test-token",
            "Content-type": 'application/json'
        })

    def test_get_payload(self):
        result = self.uma_client.get_payload(
            name='test-name',
            scopes=['test-scope'],
            optional_param='test-optional-param'
        )

        self.assertEqual(result,  {
            'name': 'test-name',
            'scopes': ['test-scope'],
            'optional_param': 'test-optional-param'
        })

        result = self.uma_client.get_payload(
            name='test-name',
            optional_param='test-optional-param'
        )

        self.assertEqual(result, {
            'name': 'test-name',
            'scopes': [],
            'optional_param': 'test-optional-param'
        })

    def test_resource_set_create(self):
        result = self.uma_client.resource_set_create(
            token='test-token',
            name='test-name',
            optional_param='test-optional-param'
        )

        self.realm.client.post.assert_called_once_with(
            'https://resource_registration',
            data=self.uma_client._get_data(
                name='test-name',
                optional_param='test-optional-param'
            ),
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.post.return_value)

    def test_resource_set_update(self):
        result = self.uma_client.resource_set_update(
            token='test-token',
            id='test-id',
            name='test-name',
            optional_param='test-optional-param'
        )

        self.realm.client.put.assert_called_once_with(
            'https://resource_registration/test-id',
            data=self.uma_client._get_data(
                name='test-name',
                optional_param='test-optional-param'
            ),
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.put.return_value)

    def test_resource_set_read(self):
        result = self.uma_client.resource_set_read(
            token='test-token',
            id='test-id',
        )

        self.realm.client.get.assert_called_once_with(
            'https://resource_registration/test-id',
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.get.return_value)

    def test_resource_set_delete(self):
        result = self.uma_client.resource_set_delete(
            token='test-token',
            id='test-id',
        )

        self.realm.client.delete.assert_called_once_with(
            'https://resource_registration/test-id',
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.delete.return_value)

    def test_resource_set_list(self):
        result = self.uma_client.resource_set_list(
            token='test-token',
            name='test-name',
            owner='test-owner'
        )

        self.realm.client.get.assert_called_once_with(
            'https://resource_registration',
            name='test-name',
            owner='test-owner',
            headers=self.uma_client.get_headers('test-token')
        )
        self.assertEqual(result, self.realm.client.get.return_value)
