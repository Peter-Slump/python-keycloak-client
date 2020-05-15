from collections.abc import Mapping
from typing import Dict, Iterator, Optional

from keycloak import client as keycloak_client


class KeycloakWellKnown(Mapping):

    _contents: Optional[Dict[str, str]] = None

    def __init__(
        self,
        client: "keycloak_client.KeycloakClient",
        path: str,
        content: Optional[Dict[str, str]] = None,
    ):
        """
        :param keycloak.realm.KeycloakRealm realm:
        :param str path: URL to find the .well-known
        :param dict | None content:
        """
        self._client: "keycloak_client.KeycloakClient" = client
        self._path: str = path
        if content:
            self._contents = content

    @property
    def contents(self) -> Dict[str, str]:
        if self._contents is None:
            self._contents = self._client.get(self._path)
        return self._contents

    @contents.setter
    def contents(self, content: Dict[str, str]) -> None:
        self._contents = content

    def __getitem__(self, key: str) -> str:
        return self.contents[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.contents)

    def __len__(self) -> int:
        return len(self.contents)
