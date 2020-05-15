import logging
from typing import Any, Dict, Union, List, Optional
from urllib.parse import urljoin


from requests import Response, Session
from requests.exceptions import HTTPError

from keycloak.exceptions import KeycloakClientError

JSONType = Union[List, Dict[str, Any], Any]


class KeycloakClient:

    _session = None

    def __init__(
        self,
        server_url: str,
        headers: Optional[Dict[str, Any]] = None,
        logger: Optional[logging.Logger] = None,
    ):
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

        self.logger: logging.Logger = logger
        self._server_url: str = server_url
        self._headers: Dict[str, Any] = headers or {}

    @property
    def server_url(self) -> str:
        return self._server_url

    @property
    def session(self) -> Session:
        """
        Get session object to benefit from connection pooling.

        http://docs.python-requests.org/en/master/user/advanced/#session-objects

        :rtype: requests.Session
        """
        if self._session is None:
            self._session = Session()
            self._session.headers.update(self._headers)
        return self._session

    def get_full_url(self, path: str, server_url: Optional[str] = None) -> str:
        return urljoin(server_url or self._server_url, path)

    def post(
        self,
        url: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, Any]] = None,
        **kwargs: Optional[Dict[str, Any]]
    ) -> JSONType:
        return self._handle_response(
            self.session.post(url, headers=headers or {}, params=kwargs, data=data)
        )

    def put(
        self,
        url: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, Any]] = None,
        **kwargs: Optional[Dict[str, Any]]
    ) -> JSONType:
        return self._handle_response(
            self.session.put(url, headers=headers or {}, params=kwargs, data=data)
        )

    def get(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs: Optional[Dict[str, Any]]
    ) -> JSONType:
        return self._handle_response(
            self.session.get(url, headers=headers or {}, params=kwargs)
        )

    def delete(
        self,
        url: str,
        headers: Optional[Dict[str, Any]],
        **kwargs: Optional[Dict[str, Any]]
    ) -> JSONType:
        return self._handle_response(
            self.session.delete(url, headers=headers, **kwargs)
        )

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

    def close(self) -> None:
        if self._session is not None:
            self._session.close()
            self._session = None

    def __enter__(self) -> "KeycloakClient":
        return self

    def __exit__(self, *args: List[Any]) -> None:
        self.close()
