from keycloak.aio.mixins import WellKnownMixin
from keycloak.authz import (
    KeycloakAuthz as SyncKeycloakAuthz,
    PATH_WELL_KNOWN,
    urlencode,
)
from keycloak.exceptions import KeycloakClientError

__all__ = (
    'KeycloakAuthz',
)


class KeycloakAuthz(WellKnownMixin, SyncKeycloakAuthz):
    def get_path_well_known(self):
        return PATH_WELL_KNOWN

    async def get_permissions(self, token, resource_scopes_tuples=None,
                              submit_request=False, ticket=None):
        """
        Request permissions for user from keycloak server.

        https://www.keycloak.org/docs/latest/authorization_services/index.html#_service_protection_permission_api_papi

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
            response = await self._realm.client.post(
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

    async def eval_permissions(self, token, resource_scopes_tuples=None,
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
        permissions = await self.get_permissions(
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
