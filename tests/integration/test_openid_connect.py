from keycloak.openid_connect import KeycloakOpenidConnect


def test_certs(openid_connect: KeycloakOpenidConnect):
    certs = openid_connect.certs()

    assert len(certs["keys"]) > 0


def test_authorization_url(openid_connect: KeycloakOpenidConnect):
    result = openid_connect.authorization_url()

    assert result.startswith("http://")
