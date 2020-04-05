import json
from typing import Dict, Optional, Union, Callable

from keycloak.realm import KeycloakRealm
from keycloak.admin.realm import Realms

__all__ = ("KeycloakAdmin", "KeycloakAdminBase")


class KeycloakAdmin(object):
    _realm: KeycloakRealm = None
    _paths: Dict[str, str] = {"root": "/"}
    _token: str = None

    def __init__(self, realm: KeycloakRealm):
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
    ) -> Dict:
        return self._realm.client.post(
            url=url, data=data, headers=self._add_auth_header(headers=headers)
        )

    def put(
        self, url: str, data: Dict, headers: Optional[dict] = None, **kwargs
    ) -> dict:
        return self._realm.client.put(
            url=url, data=data, headers=self._add_auth_header(headers=headers)
        )

    def get(self, url: str, headers: Optional[Dict] = None, **kwargs) -> Dict:
        return self._realm.client.get(
            url=url, headers=self._add_auth_header(headers=headers)
        )

    def delete(self, url: str, headers: Optional[Dict] = None, **kwargs) -> Dict:
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


class KeycloakAdminBase(object):
    _client: KeycloakAdmin = None
    _paths: Dict[str, str] = None

    def __init__(self, client: KeycloakAdmin):
        """
        Base class for Keycloak admin API end-points.
        """
        self._client = client

    def get_path(self, name: str, **kwargs) -> str:
        if self._paths is None:
            raise NotImplementedError()

        return self._paths[name].format(**kwargs)


class KeycloakAdminEntity(KeycloakAdminBase):

    _entity: Optional[Dict] = None
    _url: str = None

    def __init__(self, url: str, *args, **kwargs):
        """
        Represents a single entity as returned by the Admin API
        """
        super().__init__(*args, **kwargs)
        self._url = url

    def _get(self) -> Dict:
        return self._client.get(url=self.url)

    @property
    def entity(self) -> Dict:
        if self._entity is None:
            self._entity = self._get()
        return self._entity

    @property
    def url(self) -> str:
        return self._client.get_full_url(self._url)

    def update(self, **kwargs) -> Dict:
        """
        Updates the given entity
        Note: If the url identifier is changed by this method, url won't be changed
        """
        resp = self._client.put(url=self.url, data=json.dumps(kwargs, sort_keys=True),)
        self._entity = None
        return resp

    def delete(self):
        """
        Deleted given entity
        """
        return self._client.delete(self.url)

    def __getattr__(self, item):
        return self.entity[item]
