import warnings
from keycloak.admin import KeycloakAdmin
from keycloak.authz import KeycloakAuthz
from keycloak.client import KeycloakClient
from keycloak.openid_connect import KeycloakOpenidConnect
from keycloak.uma import KeycloakUMA
from keycloak.uma1 import KeycloakUMA1


class KeycloakRealm(object):

    _server_url = None
    _realm_name = None

    _headers = None
    _client = None

    def __init__(self, server_url, realm_name, headers=None):
        """
        :param str server_url: The base URL where the Keycloak server can be
            found
        :param str realm_name: REALM name
        :param dict headers: Optional extra headers to send with requests to
            the server
        """
        self._server_url = server_url
        self._realm_name = realm_name
        self._headers = headers

    @property
    def client(self):
        """
        :rtype: keycloak.client.KeycloakClient
        """
        if self._client is None:
            self._client = KeycloakClient(
                server_url=self._server_url, headers=self._headers
            )
        return self._client

    @property
    def realm_name(self):
        return self._realm_name

    @property
    def server_url(self):
        return self._server_url

    @property
    def admin(self):
        return KeycloakAdmin(realm=self)

    def open_id_connect(self, client_id, client_secret):
        """
        Get OpenID Connect client

        :param str client_id:
        :param str client_secret:
        :rtype: keycloak.openid_connect.KeycloakOpenidConnect
        """
        return KeycloakOpenidConnect(
            realm=self, client_id=client_id, client_secret=client_secret
        )

    def authz(self, client_id):
        """
        Get Authz client

        :param str client_id:
        :rtype: keycloak.authz.KeycloakAuthz
        """
        warnings.warn("The Authz API will be removed in Keycloak 4.0.0",
                      DeprecationWarning)
        return KeycloakAuthz(realm=self, client_id=client_id)

    def uma(self):
        """
        Get UMA client

        This method is here for backwards compatibility

        :return: keycloak.uma.KeycloakUMA
        """
        return self.uma2

    @property
    def uma2(self):
        """
        Starting from Keycloak 4 UMA2 is supported
        :rtype: keycloak.uma.KeycloakUMA
        """
        return KeycloakUMA(realm=self)

    @property
    def uma1(self):
        """
        :rtype: keycloak.uma1.KeycloakUMA1
        """
        return KeycloakUMA1(realm=self)

    def close(self):
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
