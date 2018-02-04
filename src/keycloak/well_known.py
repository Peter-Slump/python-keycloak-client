try:
    from collections import Mapping
except ImportError:
    from collections.abc import Mapping


class KeycloakWellKnown(Mapping):

    _contents = None
    _realm = None
    _path = None

    def __init__(self, realm, path, content=None):
        """
        :param keycloak.realm.KeycloakRealm realm:
        :param str url: URL to find the .well-known
        :param dict | None content:
        """
        self._realm = realm
        self._path = path
        if content:
            self._contents = content

    @property
    def contents(self):
        if self._contents is None:
            self._contents = self._realm.client.get(self._path)
        return self._contents

    @contents.setter
    def contents(self, content):
        self._contents = content

    def __getitem__(self, key):
        return self.contents[key]

    def __iter__(self):
        return iter(self.contents)

    def __len__(self):
        return len(self.contents)
