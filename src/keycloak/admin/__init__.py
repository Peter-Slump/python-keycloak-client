class KeycloakAdminBase(object):

    _client = None
    _paths = None

    def __init__(self, client):
        """
        :param keycloak.admin.KeycloakAdmin client:
        """
        self._client = client

    def get_path(self, name, **kwargs):
        if self._paths is None:
            raise NotImplementedError()

        return self._paths[name].format(**kwargs)


class KeycloakAdmin(object):

    _realm = None
    _paths = {
        'root': '/'
    }
    _token = None

    def __init__(self, realm):
        """
        :param keycloak.realm.KeycloakRealm realm:
        """
        self._realm = realm

    def root(self):
        return self.get(
            self.get_full_url(self._paths['root'])
        )

    def get_full_url(self, *args, **kwargs):
        return self._realm.client.get_full_url(*args, **kwargs)

    def set_token(self, token):
        """
        Set token to authenticate the call or a callable which will be called
        to get the token.

        :param str | callable token:
        :rtype: KeycloakAdmin
        """
        self._token = token
        return self

    @property
    def realms(self):
        from keycloak.admin.realm import Realms
        return Realms(client=self)

    def post(self, url, data, headers=None, **kwargs):
        return self._realm.client.post(
            url=url, data=data, headers=self._add_auth_header(headers=headers)
        )

    def put(self, url, data, headers=None, **kwargs):
        return self._realm.client.put(
            url=url, data=data, headers=self._add_auth_header(headers=headers)
        )

    def get(self, url, headers=None, **kwargs):
        return self._realm.client.get(
            url=url, headers=self._add_auth_header(headers=headers)
        )
    #
    # def delete(self, url, headers, **kwargs):
    #     return self.session.delete(url, headers=headers, **kwargs)

    def _add_auth_header(self, headers=None):
        if callable(self._token):
            token = self._token()
        else:
            token = self._token

        headers = headers or {}
        headers['Authorization'] = "Bearer {}".format(token)
        headers['Content-Type'] = 'application/json'
        return headers
