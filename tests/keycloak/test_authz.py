from unittest import TestCase

import mock

from keycloak.authz import KeycloakAuthz
from keycloak.realm import KeycloakRealm


class KeycloakAuthzTestCase(TestCase):

    def setUp(self):
        self.realm = mock.MagicMock(spec_set=KeycloakRealm)
        self.realm.realm_name = 'realm-name'
        self.client_id = 'client-id'

        self.authz = KeycloakAuthz(realm=self.realm, client_id=self.client_id)

    def test_entitlement(self):
        result = self.authz.entitlement(token='some-token')

        self.realm.client.get_full_url.assert_called_once_with(
            'realms/realm-name/authz/entitlement/client-id'
        )
        self.realm.client.get.assert_called_once_with(
            self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token'
            }
        )
        self.assertEqual(result, self.realm.client.get.return_value)
