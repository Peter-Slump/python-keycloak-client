from typing import Dict

import pytest

from keycloak.admin.realm import Realm
from keycloak.realm import KeycloakRealm


@pytest.mark.incremental
class TestAdminClient:

    ID = "some_client"

    @pytest.fixture()
    def admin_realm(self, realm: KeycloakRealm, client_details: Dict) -> Realm:
        token = realm.open_id_connect(
            client_id=client_details["clientId"], client_secret=client_details["secret"]
        ).client_credentials(scope="realm-management openid")

        return realm.admin.set_token(token=token).realms.by_name("test_realm")

    def test_create(self, admin_realm: Realm):
        result = admin_realm.clients.create(id=self.ID)

        assert result == b""

    def test_all(self, admin_realm: Realm):
        result = admin_realm.clients.all()

        assert any([i["clientId"] == self.ID for i in result])

    def test_by_client_id(self, admin_realm: Realm):
        result = admin_realm.clients.by_client_id(client_id=self.ID)

        assert len(result) == 1
        assert result[0]["clientId"] == self.ID

    def test_by_id(self, admin_realm: Realm):
        entity = admin_realm.clients.by_id(id=self.ID)

        assert entity.id == self.ID

    @pytest.mark.skip(reason="Results in HTTP 500")
    def test_update(self, admin_realm: Realm):
        result = admin_realm.clients.by_id(id=self.ID).update(enabled=False)

        assert result == b""

    def test_secret(self, admin_realm: Realm):
        secret = admin_realm.clients.by_id(id=self.ID).secret

        assert secret["type"] == "secret"
        assert len(secret["value"]) > 0

    @pytest.mark.skip(reason="HTTP 400; probably have to enable some setting.")
    def test_service_account_user(self, admin_realm: Realm):
        # admin_realm.clients.by_id(id=self.ID).update(service_account_enabled=False)
        user = admin_realm.clients.by_id(id=self.ID).service_account_user

        assert user.username == "Test"

    def test_delete(self, admin_realm: Realm):
        result = admin_realm.clients.by_id(id=self.ID).delete()

        assert result == b""
