from collections import OrderedDict

from keycloak.mixins import WellKnownMixin

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from jose import jwt

PATH_WELL_KNOWN = "auth/realms/{}/.well-known/openid-configuration"


class KeycloakOpenidConnect(WellKnownMixin):

    _well_known = None
    _client_id = None
    _client_secret = None
    _realm = None

    def __init__(self, realm, client_id, client_secret):
        """
        :param keycloak.realm.KeycloakRealm realm:
        :param str client_id:
        :param str client_secret:
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._realm = realm

    def get_path_well_known(self):
        return PATH_WELL_KNOWN

    def get_url(self, name):
        return self.well_known[name]

    def decode_token(self, token, key, algorithms=None, **kwargs):
        """
        A JSON Web Key (JWK) is a JavaScript Object Notation (JSON) data
        structure that represents a cryptographic key.  This specification
        also defines a JWK Set JSON data structure that represents a set of
        JWKs.  Cryptographic algorithms and identifiers for use with this
        specification are described in the separate JSON Web Algorithms (JWA)
        specification and IANA registries established by that specification.

        https://tools.ietf.org/html/rfc7517

        :param str token:
        :param str key:
        :param list | None algorithms: RS256 will be used by default.
        :return:
        """
        algorithms = algorithms or ['RS256']

        return jwt.decode(token, key, algorithms=algorithms,
                          audience=self._client_id, **kwargs)

    def logout(self, refresh_token):
        """
        The logout endpoint logs out the authenticated user.

        :param str refresh_token:
        """
        return self._realm.client.post(self.get_url('end_session_endpoint'),
                                       data={
                                           'refresh_token': refresh_token,
                                           'client_id': self._client_id,
                                           'client_secret': self._client_secret
                                       })

    def certs(self):
        """
        The certificate endpoint returns the public keys enabled by the realm,
        encoded as a JSON Web Key (JWK). Depending on the realm settings there
        can be one or more keys enabled for verifying tokens.

        https://tools.ietf.org/html/rfc7517

        :rtype: dict
        """
        return self._realm.client.get(self.get_url('jwks_uri'))

    def userinfo(self, token):
        """
        The UserInfo Endpoint is an OAuth 2.0 Protected Resource that returns
        Claims about the authenticated End-User. To obtain the requested Claims
        about the End-User, the Client makes a request to the UserInfo Endpoint
        using an Access Token obtained through OpenID Connect Authentication.
        These Claims are normally represented by a JSON object that contains a
        collection of name and value pairs for the Claims.

        http://openid.net/specs/openid-connect-core-1_0.html#UserInfo

        :param str token:
        :rtype: dict
        """
        url = self.well_known['userinfo_endpoint']

        return self._realm.client.get(url, headers={
                                          "Authorization": "Bearer {}".format(
                                              token
                                          )
                                      })

    def authorization_url(self, response_type='code', redirect_uri=None,
                          scope=None, state=None):
        """
        Get authorization URL to redirect the resource owner to.

        https://tools.ietf.org/html/rfc6749#section-4.1.1

        :param str response_type:
        :param str redirect_uri:
        :param str scope:
        :param str state:
        :return: URL to redirect the resource owner to
        :rtype: str
        """
        payload = OrderedDict()
        payload['response_type'] = response_type
        payload['client_id'] = self._client_id

        if redirect_uri:
            payload['redirect_uri'] = redirect_uri

        if scope:
            payload['scope'] = scope

        if state:
            payload['state'] = state

        params = urlencode(payload)
        url = self.get_url('authorization_endpoint')

        return '{}?{}'.format(url, params)

    def authorization_code(self, code, redirect_uri,
                           grant_type='authorization_code'):
        """
        Retrieve access token by `authorization_code` grant.

        https://tools.ietf.org/html/rfc6749#section-4.1.3

        :param str code:
        :param str redirect_uri:
        :param str grant_type:
        :rtype: dict
        """
        return self._token_request(grant_type=grant_type, code=code,
                                   redirect_uri=redirect_uri)

    def client_credentials(self, scope=None, grant_type='client_credentials'):
        """
        Retrieve access token by `client_credentials` grant.

        :param str | None scope:
        :param str grant_type:
        :rtype: dict
        """
        return self._token_request(grant_type=grant_type, scope=scope)

    def refresh_token(self, refresh_token, grant_type='refresh_token',
                      scope=None):
        """
        Refresh an access token

        https://tools.ietf.org/html/rfc6749#section-6

        :param str refresh_token:
        :param str grant_type:
        :param str \ None scope:
        :rtype: dict
        """
        if scope:
            return self._token_request(grant_type=grant_type,
                                       refresh_token=refresh_token,
                                       scope=scope)
        else:
            return self._token_request(grant_type=grant_type,
                                       refresh_token=refresh_token)

    def _token_request(self, grant_type, **kwargs):
        """
        Do the actual call to the token end-point.

        :param grant_type:
        :param kwargs:
        :return:
        """
        payload = {
            'grant_type': grant_type,
            'client_id': self._client_id,
            'client_secret': self._client_secret
        }

        payload.update(**kwargs)

        return self._realm.client.post(self.get_url('token_endpoint'),
                                       data=payload)
