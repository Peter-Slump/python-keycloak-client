from typing import Dict, Optional, Union, Callable

from keycloak.client import JSONType
from .base import KeycloakAdminBase, KeycloakAdminEntity
from .realm import Realms
from keycloak import realm

__all__ = ("KeycloakAdmin", "KeycloakAdminBase", "KeycloakAdminEntity")


class KeycloakAdmin(object):
    _realm: "realm.KeycloakRealm" = None
    _paths: Dict[str, str] = {"root": "/"}
    _token: Optional[Union[str, Callable]] = None

    def __init__(self, realm: "realm.KeycloakRealm"):
        self._realm = realm

    def root(self) -> Dict:
        return self.get(self.get_full_url(self._paths["root"]))

    def get_full_url(self, *args, **kwargs) -> str:
        return self._realm.client.get_full_url(*args, **kwargs)

    def set_token(self, token: Union[str, Callable]) -> "KeycloakAdmin":
        """
        Set token to authenticate the call or a callable which will be called
        to get the token.
        """
        self._token = token
        return self

    @property
    def realms(self) -> Realms:
        return Realms(client=self)

    def post(
        self, url: str, data: Dict, headers: Optional[Dict] = None, **kwargs
    ) -> JSONType:
        return self._realm.client.post(
            url=url, data=data, headers=self._add_auth_header(headers=headers)
        )

    def put(
        self, url: str, data: Dict, headers: Optional[dict] = None, **kwargs
    ) -> JSONType:
        return self._realm.client.put(
            url=url, data=data, headers=self._add_auth_header(headers=headers)
        )

    def get(self, url: str, headers: Optional[Dict] = None, **kwargs) -> JSONType:
        return self._realm.client.get(
            url=url, headers=self._add_auth_header(headers=headers)
        )

    def delete(self, url: str, headers: Optional[Dict] = None, **kwargs) -> JSONType:
        return self._realm.client.delete(
            url=url, headers=self._add_auth_header(headers=headers), **kwargs
        )

    def _add_auth_header(self, headers: Optional[Dict] = None) -> Dict:
        if callable(self._token):
            token = self._token()
        else:
            token = self._token

        headers = headers or {}
        headers["Authorization"] = "Bearer {}".format(token)
        headers["Content-Type"] = "application/json"
        return headers
