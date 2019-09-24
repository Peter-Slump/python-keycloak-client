import asynctest

try:
    import aiohttp  # noqa: F401
except ImportError:
    aiohttp = None
else:
    from keycloak.admin import KeycloakAdmin
    from keycloak.admin.realm import Realms
    from keycloak.aio.realm import KeycloakRealm


@asynctest.skipIf(aiohttp is None, "aiohttp is not installed")
class KeycloakAdminTestCase(asynctest.TestCase):
    def setUp(self):
        self.realm = asynctest.MagicMock(spec_set=KeycloakRealm)
        self.admin = KeycloakAdmin(realm=self.realm)

    def test_realm(self):
        realm = self.admin.realms
        self.assertIsInstance(realm, Realms)
