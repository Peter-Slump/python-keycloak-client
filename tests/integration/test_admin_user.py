from typing import Dict

import pytest

from keycloak.admin.realm import Realm
from keycloak.realm import KeycloakRealm


@pytest.mark.incremental
class TestAdminUser:

    USER_NAME = "test_user"

    @pytest.fixture()
    def admin_realm(self, realm: KeycloakRealm, client_details: Dict) -> Realm:
        token = realm.open_id_connect(
            client_id=client_details["clientId"], client_secret=client_details["secret"]
        ).client_credentials(scope="realm-management openid")

        return realm.admin.set_token(token=token).realms.by_name("test_realm")

    def test_create(self, admin_realm: Realm):
        result = admin_realm.users.create(
            username=self.USER_NAME, password="TestPassword"
        )

        assert result == b""

    def test_all(self, admin_realm: Realm):
        result = admin_realm.users.all()

        assert len(result) == 1
        assert result[0]["username"] == self.USER_NAME

    @pytest.mark.dependency()
    def test_by_username(self, admin_realm: Realm):
        entity = admin_realm.users.by_username(username=self.USER_NAME)

        assert entity.username == "test_user"

    @pytest.mark.dependency(depends=["TestAdminUser::test_by_username"])
    def test_by_id(self, admin_realm: Realm):
        entity = admin_realm.users.by_username(username=self.USER_NAME)

        user = admin_realm.users.by_id(user_id=entity.id)

        assert user.username == "test_user"

    @pytest.mark.dependency(depends=["TestAdminUser::test_by_username"])
    def test_update(self, admin_realm: Realm):
        entity = admin_realm.users.by_username(username=self.USER_NAME)

        result = entity.update(first_name="John", last_name="Doe")

        assert result == b""

    @pytest.mark.dependency(depends=["TestAdminUser::test_by_username"])
    def test_reset_password(self, admin_realm: Realm):
        entity = admin_realm.users.by_username(username=self.USER_NAME)

        result = entity.reset_password(password="OtherUnsecurePassword")

        assert result == b""

    def test_delete(self, admin_realm: Realm):
        entity = admin_realm.users.by_username(username=self.USER_NAME)

        result = entity.delete()

        assert result == b""
