import requests

try:
    from collections import Mapping
except ImportError:
    from collections.abc import Mapping


class KeycloakWellKnown(Mapping):

    _contents = None
    _url = None

    def __init__(self, url, content=None):
        """
        :param str url: URL to find the .well-known
        :param dict | None content:
        """
        self._url = url
        if content:
            self._contents = content

    @property
    def contents(self):
        if self._contents is None:
            response = requests.get(self._url)
            self._contents = response.json()
        return self._contents

    def __getitem__(self, key):
        return self.contents[key]

    def __iter__(self):
        return iter(self.contents)

    def __len__(self):
        return len(self.contents)
