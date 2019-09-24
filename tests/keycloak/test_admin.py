from unittest import TestCase

import mock

from keycloak.admin import KeycloakAdmin
from keycloak.admin.realm import Realms
from keycloak.realm import KeycloakRealm


class KeycloakAdminTestCase(TestCase):
    def setUp(self):
        self.realm = mock.MagicMock(spec_set=KeycloakRealm)
        self.admin = KeycloakAdmin(realm=self.realm)

    def test_realm(self):
        realm = self.admin.realms
        self.assertIsInstance(realm, Realms)
