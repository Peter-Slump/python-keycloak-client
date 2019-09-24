from unittest import TestCase

import mock

from keycloak.admin import KeycloakAdmin
from keycloak.authz import KeycloakAuthz
from keycloak.client import KeycloakClient
from keycloak.openid_connect import KeycloakOpenidConnect
from keycloak.realm import KeycloakRealm
from keycloak.uma import KeycloakUMA


class KeycloakRealmTestCase(TestCase):
    def setUp(self):
        self.realm = KeycloakRealm(
            "https://example.com", "some-realm", headers={"some": "header"}
        )

    def test_instance(self):
        """
        Case: Realm is instantiated
        Expected: Name and server_url are exposed
        """
        self.assertEqual(self.realm.realm_name, "some-realm")
        self.assertEqual(self.realm.server_url, "https://example.com")

    @mock.patch("keycloak.realm.KeycloakClient", autospec=True)
    def test_client(self, mocked_client):
        """
        Case: Client get requested
        Expected: Client get returned and the second time the same get returned
        """
        client = self.realm.client

        self.assertIsInstance(client, KeycloakClient)

        self.assertEqual(client, self.realm.client)

        mocked_client.assert_called_once_with(
            server_url="https://example.com", headers={"some": "header"}
        )

    @mock.patch("keycloak.realm.KeycloakOpenidConnect", autospec=True)
    def test_openid_connect(self, mocked_openid_client):
        """
        Case: OpenID client get requested
        Expected: OpenID client get returned
        """
        openid_client = self.realm.open_id_connect(
            client_id="client-id", client_secret="client-secret"
        )

        self.assertIsInstance(openid_client, KeycloakOpenidConnect)
        self.assertEqual(openid_client, mocked_openid_client.return_value)
        mocked_openid_client.assert_called_once_with(
            realm=self.realm, client_id="client-id", client_secret="client-secret"
        )

    @mock.patch("keycloak.realm.KeycloakAdmin", autospec=True)
    def test_admin(self, mocked_admin_client):
        """
        Case: Admin client get requested
        Expected: Admin client get returned
        """
        admin_client = self.realm.admin
        self.assertIsInstance(admin_client, KeycloakAdmin)
        mocked_admin_client.assert_called_once_with(realm=self.realm)

    @mock.patch("keycloak.realm.KeycloakAuthz", autospec=True)
    def test_authz(self, mocked_authz_client):
        """
        Case: Authz client get requested
        Expected: Authz client get returned
        """
        authz_client = self.realm.authz(client_id="client-id")

        self.assertIsInstance(authz_client, KeycloakAuthz)
        mocked_authz_client.assert_called_once_with(
            realm=self.realm, client_id="client-id"
        )

    @mock.patch("keycloak.realm.KeycloakUMA", autospec=True)
    def test_uma(self, mocked_uma_client):
        """
        Case: UMA client get requested
        Expected: UMA client get returned
        """
        uma_client = self.realm.uma()

        self.assertIsInstance(uma_client, KeycloakUMA)
        mocked_uma_client.assert_called_once_with(realm=self.realm)
