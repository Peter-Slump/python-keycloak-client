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

        :param str token: A signed JWS to be verified.
        :param str key: A key to attempt to verify the payload with.
        :param str,list algorithms: (optional) Valid algorithms that should be
            used to verify the JWS. Defaults to `['RS256']`
        :param str audience: (optional) The intended audience of the token. If
            the "aud" claim is included in the claim set, then the audience
            must be included and must equal the provided claim.
        :param str,iterable issuer: (optional) Acceptable value(s) for the
            issuer of the token. If the "iss" claim is included in the claim
            set, then the issuer must be given and the claim in the token must
            be among the acceptable values.
        :param str subject: (optional) The subject of the token. If the "sub"
            claim is included in the claim set, then the subject must be
            included and must equal the provided claim.
        :param str access_token: (optional) An access token returned alongside
            the id_token during the authorization grant flow. If the "at_hash"
            claim is included in the claim set, then the access_token must be
            included, and it must match the "at_hash" claim.
        :param dict options: (optional) A dictionary of options for skipping
            validation steps.
            defaults:

             .. code-block:: python

                 {
                    'verify_signature': True,
                    'verify_aud': True,
                    'verify_iat': True,
                    'verify_exp': True,
                    'verify_nbf': True,
                    'verify_iss': True,
                    'verify_sub': True,
                    'verify_jti': True,
                    'leeway': 0,
                }

        :return: The dict representation of the claims set, assuming the
            signature is valid and all requested data validation passes.
        :rtype: dict
        :raises jose.exceptions.JWTError: If the signature is invalid in any
            way.
        :raises jose.exceptions.ExpiredSignatureError: If the signature has
            expired.
        :raises jose.exceptions.JWTClaimsError: If any claim is invalid in any
            way.
        """
        return jwt.decode(token, key,
                          audience=kwargs.get('audience') or self._client_id,
                          algorithms=algorithms or ['RS256'], **kwargs)

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

    def authorization_url(self, **kwargs):
        """
        Get authorization URL to redirect the resource owner to.

        https://tools.ietf.org/html/rfc6749#section-4.1.1

        :param str redirect_uri: (optional) Absolute URL of the client where
            the user-agent will be redirected to.
        :param str scope: (optional) Space delimited list of strings.
        :param str state: (optional) An opaque value used by the client to
            maintain state between the request and callback
        :return: URL to redirect the resource owner to
        :rtype: str
        """
        payload = OrderedDict()
        payload['response_type'] = 'code'
        payload['client_id'] = self._client_id

        for key in sorted(kwargs.keys()):
            # Add items in a sorted way for unittest purposes.
            payload[key] = kwargs[key]

        params = urlencode(payload)
        url = self.get_url('authorization_endpoint')

        return '{}?{}'.format(url, params)

    def authorization_code(self, code, redirect_uri):
        """
        Retrieve access token by `authorization_code` grant.

        https://tools.ietf.org/html/rfc6749#section-4.1.3

        :param str code: The authorization code received from the authorization
            server.
        :param str redirect_uri: the identical value of the "redirect_uri"
            parameter in the authorization request.
        :rtype: dict
        :return: Access token response
        """
        return self._token_request(grant_type='authorization_code', code=code,
                                   redirect_uri=redirect_uri)

    def client_credentials(self, **kwargs):
        """
        Retrieve access token by `client_credentials` grant.

        https://tools.ietf.org/html/rfc6749#section-4.4

        :param str scope: (optional) Space delimited list of strings.
        :rtype: dict
        :return: Access token response
        """
        return self._token_request(grant_type='client_credentials', **kwargs)

    def refresh_token(self, refresh_token, **kwargs):
        """
        Refresh an access token

        https://tools.ietf.org/html/rfc6749#section-6

        :param str refresh_token:
        :param str scope: (optional) Space delimited list of strings.
        :rtype: dict
        :return: Access token response
        """
        return self._token_request(grant_type='refresh_token',
                                   refresh_token=refresh_token, **kwargs)

    def token_exchange(self, **kwargs):
        """
        Token exchange is the process of using a set of credentials or token to
        obtain an entirely different token.

        http://www.keycloak.org/docs/latest/securing_apps/index.html#_token-exchange
        https://www.ietf.org/id/draft-ietf-oauth-token-exchange-12.txt

        :param subject_token: A security token that represents the identity of
            the party on behalf of whom the request is being made. It is
            required if you are exchanging an existing token for a new one.
        :param subject_issuer: Identifies the issuer of the subject_token. It
            can be left blank if the token comes from the current realm or if
            the issuer can be determined from the subject_token_type. Otherwise
            it is required to be specified. Valid values are the alias of an
            Identity Provider configured for your realm. Or an issuer claim
            identifier configured by a specific Identity Provider.
        :param subject_token_type: This parameter is the type of the token
            passed with the subject_token parameter. This defaults to
            urn\:ietf:params:oauth:token-type:access_token if the subject_token
            comes from the realm and is an access token. If it is an external
            token, this parameter may or may not have to be specified depending
            on the requirements of the subject_issuer.
        :param requested_token_type:  This parameter represents the type of
            token the client wants to exchange for. Currently only oauth and
            OpenID Connect token types are supported. The default value for
            this depends on whether the is
            urn:ietf:params:oauth:token-type:refresh_token in which case you
            will be returned both an access token and refresh token within the
            response. Other appropriate values are
            urn\:ietf:params:oauth:token-type:access_token and
            urn\:ietf:params:oauth:token-type:id_token
        :param audience: This parameter specifies the target client you want
            the new token minted for.
        :param requested_issuer: This parameter specifies that the client wants
            a token minted by an external provider. It must be the alias of an
            Identity Provider configured within the realm.
        :param requested_subject: This specifies a username or user id if your
            client wants to impersonate a different user.
        :rtype: dict
        :return: access_token, refresh_token and expires_in
        """
        return self._token_request(
            grant_type='urn:ietf:params:oauth:grant-type:token-exchange',
            **kwargs
        )

    def _token_request(self, grant_type, **kwargs):
        """
        Do the actual call to the token end-point.

        :param grant_type:
        :param kwargs: See invoking methods.
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
