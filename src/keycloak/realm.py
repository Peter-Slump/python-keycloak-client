from keycloak.admin import KeycloakAdmin
from keycloak.authz import KeycloakAuthz
from keycloak.client import KeycloakClient
from keycloak.openid_connect import KeycloakOpenidConnect
from keycloak.uma import KeycloakUMA


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
            self._client = KeycloakClient(server_url=self._server_url,
                                          headers=self._headers)
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
        return KeycloakOpenidConnect(realm=self, client_id=client_id,
                                     client_secret=client_secret)

    def authz(self, client_id):
        """
        Get Authz client

        :param str client_id:
        :rtype: keycloak.authz.KeycloakAuthz
        """
        return KeycloakAuthz(realm=self, client_id=client_id)

    def uma(self):
        """
        Get UMA client
        :return: keycloak.uma.KeycloakUMA
        """
        return KeycloakUMA(realm=self)
