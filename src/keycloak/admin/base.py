import json
from typing import Any, Dict, Optional

from keycloak import admin
from keycloak.client import JSONType


def to_camel_case(snake_cased_str: str) -> str:
    components = snake_cased_str.split("_")
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + "".join(map(str.capitalize, components[1:]))


class KeycloakAdminBase:
    _client: "admin.KeycloakAdmin" = None
    _paths: Optional[Dict[str, str]] = None

    def __init__(self, client: "admin.KeycloakAdmin"):
        """
        Base class for Keycloak admin API end-points.
        """
        self._client = client

    def get_path(self, name: str, **kwargs: Any) -> str:
        if self._paths is None:
            raise NotImplementedError()

        return self._paths[name].format(**kwargs)


class KeycloakAdminEntity(KeycloakAdminBase):

    _entity: Optional[JSONType] = None

    def __init__(self, url: str, *args: Any, **kwargs: Any):
        """
        Represents a single entity as returned by the Admin API
        """
        super().__init__(*args, **kwargs)
        self._url: str = url

    def _get(self) -> JSONType:
        return self._client.get(url=self.url)

    @property
    def entity(self) -> JSONType:
        if self._entity is None:
            self._entity = self._get()
        return self._entity

    @property
    def url(self) -> str:
        return self._client.get_full_url(self._url)

    def update(self, **kwargs: Any) -> JSONType:
        """
        Updates the given entity
        Note: If the url identifier is changed by this method, url won't be changed
        """
        data = {to_camel_case(key): value for key, value in kwargs.items()}

        resp = self._client.put(
            url=self.url, data=json.dumps(data, sort_keys=True),
        )
        self._entity = None
        return resp

    def delete(self) -> JSONType:
        """
        Deleted given entity
        """
        return self._client.delete(self.url)

    def __getattr__(self, item: str) -> Any:
        return self.entity[item]
