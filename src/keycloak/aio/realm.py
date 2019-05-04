import asyncio

from keycloak.aio.abc import AsyncInit
from keycloak.aio.authz import KeycloakAuthz
from keycloak.aio.client import KeycloakClient
from keycloak.aio.openid_connect import KeycloakOpenidConnect
from keycloak.aio.uma import KeycloakUMA
from keycloak.realm import KeycloakRealm as SyncKeycloakRealm

__all__ = (
    'KeycloakRealm',
)


class KeycloakRealm(AsyncInit, SyncKeycloakRealm):
    _lock = None
    _loop = None

    def __init__(self, *args, loop=None, **kwargs):
        self.client_class = kwargs.pop('client_class', KeycloakClient)
        super().__init__(*args, **kwargs)
        self._lock = asyncio.Lock()
        self._loop = loop or asyncio.get_event_loop()

    @property
    def client(self):
        """
        Get Keycloak client

        :rtype: keycloak.aio.client.KeycloakClient
        """
        if self._client is None:
            raise RuntimeError
        return self._client

    def open_id_connect(self, client_id, client_secret):
        """
        Get OpenID Connect client

        :param str client_id:
        :param str client_secret:
        :rtype: keycloak.aio.openid_connect.KeycloakOpenidConnect
        """
        return KeycloakOpenidConnect(realm=self, client_id=client_id,
                                     client_secret=client_secret)

    def authz(self, client_id):
        """
        Get async Authz client

        :param str client_id:
        :rtype: keycloak.aio.authz.KeycloakAuthz
        """
        return KeycloakAuthz(realm=self, client_id=client_id)

    def uma(self):
        """
        Get UMA client
        :return: keycloak.aio.uma.KeycloakUMA
        """
        return KeycloakUMA(realm=self)

    async def __async_init__(self) -> 'KeycloakRealm':
        async with self._lock:
            if self._client is None:
                self._client = await self.client_class(
                    server_url=self._server_url,
                    headers=self._headers,
                    loop=self._loop
                )
        return self

    async def close(self):
        if self._client is not None:
            await self._client.close()
            self._client = None
