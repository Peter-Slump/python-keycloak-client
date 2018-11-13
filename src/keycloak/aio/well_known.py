from keycloak.aio.abc import AsyncInit
from ..well_known import KeycloakWellKnown as SyncKeycloakWellKnown

__all__ = (
    'KeycloakWellKnown',
)


class KeycloakWellKnown(AsyncInit, SyncKeycloakWellKnown):
    @property
    def contents(self):
        if self._contents is None:
            raise RuntimeError
        return self._contents

    @contents.setter
    def contents(self, content):
        self._contents = content

    async def __async_init__(self) -> 'KeycloakWellKnown':
        async with self._realm.client._lock:
            if self._contents is None:
                self._contents = await self._realm.client.get(self._path)
        return self

    async def close(self):
        pass
