import logging
from typing import Any, Dict
from urllib.parse import urljoin

import requests
from requests import Response
from requests.exceptions import HTTPError

from keycloak.exceptions import KeycloakClientError

JSONType = Dict[str, Any]


class KeycloakClient:
    _server_url = None
    _session = None
    _headers = None

    def __init__(self, server_url, headers=None, logger=None):
        """
         :param str server_url: The base URL where the Keycloak server can be
            found
        :param dict headers: Optional extra headers to send with requests to
            the server
        :param logging.Logger logger: Optional logger for client
        """
        if logger is None:
            if hasattr(self.__class__, "__qualname__"):
                logger_name = self.__class__.__qualname__
            else:
                logger_name = self.__class__.__name__

            logger = logging.getLogger(logger_name)

        self.logger = logger
        self._server_url = server_url
        self._headers = headers or {}

    @property
    def server_url(self):
        return self._server_url

    @property
    def session(self):
        """
        Get session object to benefit from connection pooling.

        http://docs.python-requests.org/en/master/user/advanced/#session-objects

        :rtype: requests.Session
        """
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update(self._headers)
        return self._session

    def get_full_url(self, path, server_url=None) -> str:
        return urljoin(server_url or self._server_url, path)

    def post(self, url, data, headers=None, **kwargs):
        return self._handle_response(
            self.session.post(url, headers=headers or {}, params=kwargs, data=data)
        )

    def put(self, url, data, headers=None, **kwargs):
        return self._handle_response(
            self.session.put(url, headers=headers or {}, params=kwargs, data=data)
        )

    def get(self, url, headers=None, **kwargs):
        return self._handle_response(
            self.session.get(url, headers=headers or {}, params=kwargs)
        )

    def delete(self, url, headers, **kwargs):
        return self.session.delete(url, headers=headers, **kwargs)

    def _handle_response(self, response: Response) -> JSONType:
        with response:
            try:
                response.raise_for_status()
            except HTTPError as err:
                self.logger.debug(response.content)
                self.logger.debug(response.headers)
                self.logger.debug(response.request.headers)
                raise KeycloakClientError(original_exc=err)

            try:
                return response.json()
            except ValueError:
                return response.content

    def close(self):
        if self._session is not None:
            self._session.close()
            self._session = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
