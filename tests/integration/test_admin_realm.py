from typing import Dict

import pytest

from keycloak.admin import Realms
from keycloak.realm import KeycloakRealm


@pytest.mark.incremental()
class TestAdminRealm:

    NAME = "test_realm"

    @pytest.fixture()
    def admin_realms(self, realm: KeycloakRealm, client_details: Dict) -> Realms:
        token = realm.open_id_connect(
            client_id=client_details["clientId"],
            client_secret=client_details["secret"],
        ).client_credentials(scope="realm-management openid")

        return realm.admin.set_token(token=token).realms

    @pytest.mark.skip(reason="No permissions")
    def test_create(self, admin_realms: Realms):
        result = admin_realms.create(name=self.NAME)

        assert result == b""

    def test_all(self, admin_realms: Realms):

        result = admin_realms.all()

        assert len(result) == 1
        assert result[0]["realm"] == self.NAME

    def test_by_name(self, admin_realms: Realms):
        entity = admin_realms.by_name(name=self.NAME)

        assert entity.realm == self.NAME

    def test_update(self, admin_realms: Realms):
        entity = admin_realms.by_name(name=self.NAME)

        result = entity.update(display_name="Some Realm")

        assert result == b""

    @pytest.mark.skip(
        reason="This breaks other tests which are dependant on this realm"
    )
    def test_delete(self, admin_realms: Realms):
        entity = admin_realms.by_name(name=self.NAME)

        result = entity.delete()

        assert result == b""
