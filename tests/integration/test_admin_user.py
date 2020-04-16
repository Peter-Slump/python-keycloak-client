from typing import Dict

import pytest

from keycloak.admin.realm import Realm
from keycloak.realm import KeycloakRealm


@pytest.fixture()
def admin_realm(realm: KeycloakRealm, client_details: Dict) -> Realm:
    token = realm.open_id_connect(
        client_id=client_details["clientId"], client_secret=client_details["secret"]
    ).client_credentials(scope="realm-management openid")

    return realm.admin.set_token(token=token).realms.by_name("test_realm")


def test_create(admin_realm: Realm):
    result = admin_realm.users.create(username="test_user", password="TestPassword")

    assert result == b""
