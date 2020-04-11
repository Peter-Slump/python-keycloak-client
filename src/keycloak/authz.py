import base64
import json
import logging
from typing import Dict, Any, Iterable, Tuple, Optional

from urllib.parse import urlencode

from keycloak import realm as keycloak_realm
from keycloak.client import JSONType
from keycloak.mixins import WellKnownMixin
from keycloak.exceptions import KeycloakClientError

PATH_ENTITLEMENT = "auth/realms/{}/authz/entitlement/{}"

PATH_WELL_KNOWN = "auth/realms/{}/.well-known/uma2-configuration"

logger = logging.getLogger(__name__)


class KeycloakAuthz(WellKnownMixin):
    def __init__(self, realm: "keycloak_realm.KeycloakRealm", client_id: str):
        self._realm: "keycloak_realm.KeycloakRealm" = realm
        self._client_id: str = client_id

    def get_path_well_known(self):
        return PATH_WELL_KNOWN

    def entitlement(self, token: str) -> JSONType:
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
    def _decode_token(cls, token: str) -> Dict[str, Any]:
        """
        Permission information is encoded in an authorization token.
        """
        missing_padding = len(token) % 4
        if missing_padding != 0:
            token += "=" * (4 - missing_padding)
        return json.loads(base64.b64decode(token).decode("utf-8"))

    def get_permissions(
        self,
        token: str,
        resource_scopes_tuples: Optional[Iterable[Tuple[str, str]]] = None,
        submit_request: Optional[bool] = False,
        ticket: Optional[str] = None,
    ) -> Dict[str, Any]:
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
            "Content-type": "application/x-www-form-urlencoded",
        }

        data = [
            ("grant_type", "urn:ietf:params:oauth:grant-type:uma-ticket"),
            ("audience", self._client_id),
            ("response_include_resource_name", True),
        ]

        if resource_scopes_tuples:
            for atuple in resource_scopes_tuples:
                data.append(("permission", "#".join(atuple)))
            data.append(("submit_request", submit_request))
        elif ticket:
            data.append(("ticket", ticket))

        authz_info = {}

        try:
            response = self._realm.client.post(
                self.well_known["token_endpoint"], data=urlencode(data), headers=headers
            )

            error = response.get("error")
            if error:
                logger.warning("%s: %s", error, response.get("error_description"))
            else:
                token = response.get("refresh_token")
                decoded_token = self._decode_token(token.split(".")[1])
                authz_info = decoded_token.get("authorization", {})
        except KeycloakClientError as error:
            logger.warning(str(error))
        return authz_info

    def eval_permission(
        self, token: str, resource: str, scope: str, submit_request=False
    ):
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
            submit_request=submit_request,
        )

    def eval_permissions(
        self,
        token: str,
        resource_scopes_tuples: Optional[Iterable[Tuple[str, str]]] = None,
        submit_request: Optional[bool] = False,
    ) -> bool:
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
            submit_request=submit_request,
        )

        res = []
        for permission in permissions.get("permissions", []):
            for scope in permission.get("scopes", []):
                ptuple = (permission.get("rsname"), scope)
                if ptuple in resource_scopes_tuples:
                    res.append(ptuple)

        return res == resource_scopes_tuples
