from typing import Optional, Dict, Any

from keycloak import admin
from keycloak.authz import KeycloakAuthz
from keycloak.client import KeycloakClient
from keycloak.openid_connect import KeycloakOpenidConnect
from keycloak.uma import KeycloakUMA
from keycloak.uma1 import KeycloakUMA1


class KeycloakRealm:

    _client: Optional[KeycloakClient] = None

    def __init__(
        self, server_url: str, realm_name: str, headers: Optional[Dict[str, Any]] = None
    ):
        """
        :param str server_url: The base URL where the Keycloak server can be
            found
        :param str realm_name: REALM name
        :param dict headers: Optional extra headers to send with requests to
            the server
        """
        self._server_url: str = server_url
        self._realm_name = realm_name
        self._headers = headers

    @property
    def client(self) -> KeycloakClient:
        """
        :rtype: keycloak.client.KeycloakClient
        """
        if self._client is None:
            self._client = KeycloakClient(
                server_url=self._server_url, headers=self._headers
            )
        return self._client

    @property
    def realm_name(self) -> str:
        return self._realm_name

    @property
    def server_url(self) -> str:
        return self._server_url

    @property
    def admin(self) -> "admin.KeycloakAdmin":
        return admin.KeycloakAdmin(realm=self)

    def open_id_connect(
        self, client_id: str, client_secret: str
    ) -> KeycloakOpenidConnect:
        """
        Get OpenID Connect client

        :param str client_id:
        :param str client_secret:
        :rtype: keycloak.openid_connect.KeycloakOpenidConnect
        """
        return KeycloakOpenidConnect(
            realm=self, client_id=client_id, client_secret=client_secret
        )

    def authz(self, client_id: str) -> KeycloakAuthz:
        """
        Get Authz client

        :param str client_id:
        :rtype: keycloak.authz.KeycloakAuthz
        """
        return KeycloakAuthz(realm=self, client_id=client_id)

    def uma(self) -> KeycloakUMA:
        """
        Get UMA client

        This method is here for backwards compatibility

        :return: keycloak.uma.KeycloakUMA
        """
        return self.uma2

    @property
    def uma2(self) -> KeycloakUMA:
        """
        Starting from Keycloak 4 UMA2 is supported
        :rtype: keycloak.uma.KeycloakUMA
        """
        return KeycloakUMA(realm=self)

    @property
    def uma1(self) -> KeycloakUMA1:
        """
        :rtype: keycloak.uma1.KeycloakUMA1
        """
        return KeycloakUMA1(realm=self)

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> "KeycloakRealm":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
