from requests.exceptions import HTTPError

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests


class KeycloakClient(object):

    _server_url = None
    _session = None
    _headers = None

    def __init__(self, server_url, headers=None):
        self._server_url = server_url
        self._headers = headers or {}

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

    def get_full_url(self, path, server_url=None):
        return urljoin(server_url or self._server_url, path)

    def post(self, url, data, headers=None, **kwargs):
        return self._handle_response(
            self.session.post(url, headers=headers or {}, params=kwargs,
                              data=data)
        )

    def get(self, url, headers=None, **kwargs):
        return self._handle_response(
            self.session.get(url, headers=headers or {}, params=kwargs)
        )

    def _handle_response(self, response):
        try:
            response.raise_for_status()
        except HTTPError as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.debug(response.content)
            logger.debug(response.request.headers)
            raise

        try:
            return response.json()
        except ValueError:
            return response.content
