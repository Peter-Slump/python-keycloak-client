import asyncio
from functools import partial
from typing import Any

import aiohttp

from keycloak.aio.abc import AsyncInit
from keycloak.client import KeycloakClient as SyncKeycloakClient
from keycloak.exceptions import KeycloakClientError

__all__ = (
    'KeycloakClient',
)


class KeycloakClient(AsyncInit, SyncKeycloakClient):
    _lock = None
    _loop = None
    _session_factory = None

    def __init__(self, server_url, *, headers, logger=None, loop=None,
                 session_factory=aiohttp.client.ClientSession,
                 **session_params):

        super().__init__(server_url, headers=headers, logger=logger)

        self._lock = asyncio.Lock()
        self._loop = loop or asyncio.get_event_loop()

        session_params['loop'] = self._loop
        session_params['headers'] = self._headers
        self._session_factory = partial(session_factory, **session_params)

    @property
    def loop(self):
        return self._loop

    @property
    def session(self):
        if not self._session:
            raise RuntimeError
        return self._session

    async def _handle_response(self, req_ctx) -> Any:
        """
        :param aiohttp.client._RequestContextManager req_ctx
        :return:
        """
        async with req_ctx as response:
            try:
                response.raise_for_status()
            except aiohttp.client.ClientResponseError as cre:
                text = await response.text(errors='replace')
                self.logger.debug('{cre}; '
                                  'Request info: {cre.request_info}; '
                                  'Response headers: {cre.headers}; '
                                  'Response status: {cre.status}; '
                                  'Content: {text}'.format(cre=cre, text=text))
                raise KeycloakClientError(original_exc=cre)

            try:
                result = await response.json(content_type=None)
            except ValueError:
                result = await response.read()

        return result

    async def __async_init__(self) -> 'KeycloakClient':
        async with self._lock:
            if self._session is None:
                self._session = self._session_factory()
                await self._session.__aenter__()
        return self

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None
