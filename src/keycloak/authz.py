import base64
import json
import logging

try:
    from urllib.parse import urlencode  # noqa: F401
except ImportError:
    from urllib import urlencode  # noqa: F401

from keycloak.mixins import WellKnownMixin
from keycloak.exceptions import KeycloakClientError

PATH_ENTITLEMENT = "auth/realms/{}/authz/entitlement/{}"

PATH_WELL_KNOWN = "auth/realms/{}/.well-known/uma2-configuration"


class KeycloakAuthz(WellKnownMixin, object):
    _realm = None
    _client_id = None
    _well_known = None

    logger = logging.getLogger(__name__)

    def __init__(self, realm, client_id):
        """

        :param keycloak.realm.KeycloakRealm realm:
        :param client_id:
        """
        self._realm = realm
        self._client_id = client_id

    def get_path_well_known(self):
        return PATH_WELL_KNOWN

    def entitlement(self, token):
        """
        Client applications can use a specific endpoint to obtain a special
        security token called a requesting party token (RPT). This token
        consists of all the entitlements (or permissions) for a user as a
        result of the evaluation of the permissions and authorization policies
        associated with the resources being requested. With an RPT, client
        applications can gain access to protected resources at the resource
        server.

        http://www.keycloak.org/docs/latest/authorization_services/index
        .html#_service_entitlement_api

        :rtype: dict
        """
        headers = {"Authorization": "Bearer %s" % token}
        url = self._realm.client.get_full_url(
            PATH_ENTITLEMENT.format(self._realm.realm_name, self._client_id)
        )
        return self._realm.client.get(url, headers=headers)

    @classmethod
    def _decode_token(cls, token):
        """
        Permission information is encoded in an authorization token.
        """
        missing_padding = len(token) % 4
        if missing_padding != 0:
            token += '=' * (4 - missing_padding)
        return json.loads(base64.b64decode(token).decode('utf-8'))

    def get_permissions(self, token, resource_scopes_tuples=None,
                        submit_request=False, ticket=None):
        """
        Request permissions for user from keycloak server.

        https://www.keycloak.org/docs/latest/authorization_services/index
        .html#_service_protection_permission_api_papi

        :param str token: client access token
        :param Iterable[Tuple[str, str]] resource_scopes_tuples:
            list of tuples (resource, scope)
        :param boolean submit_request: submit request if not allowed to access?
        :param str ticket: Permissions ticket
        rtype: dict
        """
        headers = {
            "Authorization": "Bearer %s" % token,
            'Content-type': 'application/x-www-form-urlencoded',
        }

        data = [
            ('grant_type', 'urn:ietf:params:oauth:grant-type:uma-ticket'),
            ('audience', self._client_id),
            ('response_include_resource_name', True),
        ]

        if resource_scopes_tuples:
            for atuple in resource_scopes_tuples:
                data.append(('permission', '#'.join(atuple)))
            data.append(('submit_request', submit_request))
        elif ticket:
            data.append(('ticket', ticket))

        authz_info = {}

        try:
            response = self._realm.client.post(
                self.well_known['token_endpoint'],
                data=urlencode(data),
                headers=headers,
            )

            error = response.get('error')
            if error:
                self.logger.warning(
                    '%s: %s',
                    error,
                    response.get('error_description')
                )
            else:
                token = response.get('refresh_token')
                decoded_token = self._decode_token(token.split('.')[1])
                authz_info = decoded_token.get('authorization', {})
        except KeycloakClientError as error:
            self.logger.warning(str(error))
        return authz_info

    def eval_permission(self, token, resource, scope, submit_request=False):
        """
        Evalutes if user has permission for scope on resource.

        :param str token: client access token
        :param str resource: resource to access
        :param str scope: scope on resource
        :param boolean submit_request: submit request if not allowed to access?
        rtype: boolean
        """
        return self.eval_permissions(
            token=token,
            resource_scopes_tuples=[(resource, scope)],
            submit_request=submit_request
        )

    def eval_permissions(self, token, resource_scopes_tuples=None,
                         submit_request=False):
        """
        Evaluates if user has permission for all the resource scope
        combinations.

        :param str token: client access token
        :param Iterable[Tuple[str, str]] resource_scopes_tuples: resource to
        access
        :param boolean submit_request: submit request if not allowed to access?
        rtype: boolean
        """
        permissions = self.get_permissions(
            token=token,
            resource_scopes_tuples=resource_scopes_tuples,
            submit_request=submit_request
        )

        res = []
        for permission in permissions.get('permissions', []):
            for scope in permission.get('scopes', []):
                ptuple = (permission.get('rsname'), scope)
                if ptuple in resource_scopes_tuples:
                    res.append(ptuple)

        return res == resource_scopes_tuples
