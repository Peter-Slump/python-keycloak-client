import json
from typing import Dict, Any, Optional, List

from keycloak import realm as keycloak_realm
from keycloak.client import JSONType
from keycloak.mixins import WellKnownMixin

PATH_WELL_KNOWN = "auth/realms/{}/.well-known/uma-configuration"


class KeycloakUMA1(WellKnownMixin):
    DEFAULT_HEADERS: Dict[str, str] = {"Content-type": "application/json"}

    _dumps = staticmethod(json.dumps)

    def __init__(self, realm: "keycloak_realm.KeycloakRealm"):
        """
        :type realm: keycloak.realm.KeycloakRealm
        """
        self._realm: "keycloak_realm.KeycloakRealm" = realm

    def get_path_well_known(self) -> str:
        return PATH_WELL_KNOWN

    def resource_set_create(self, token: str, name: str, **kwargs: Any) -> JSONType:
        """
        Create a resource set.

        https://docs.kantarainitiative.org/uma/rec-oauth-resource-reg-v1_0_1.html#rfc.section.2.2.1

        :param str token: client access token
        :param str name:
        :param str uri: (optional)
        :param str type: (optional)
        :param list scopes: (optional)
        :param str icon_uri: (optional)
        :rtype: str
        """
        return self._realm.client.post(
            self.well_known["resource_set_registration_endpoint"],
            data=self._get_data(name=name, **kwargs),
            headers=self.get_headers(token),
        )

    def resource_set_update(
        self, token: str, id: str, name: str, **kwargs: Any
    ) -> JSONType:
        """
        Update a resource set.

        https://docs.kantarainitiative.org/uma/rec-oauth-resource-reg-v1_0_1.html#update-resource-set

        :param str token: client access token
        :param str id: Identifier of the resource set
        :param str name:
        :param str uri: (optional)
        :param str type: (optional)
        :param list scopes: (optional)
        :param str icon_uri: (optional)
        :rtype: str
        """
        return self._realm.client.put(
            "{}/{}".format(self.well_known["resource_set_registration_endpoint"], id),
            data=self._get_data(name=name, **kwargs),
            headers=self.get_headers(token),
        )

    def resource_set_read(self, token: str, id: str) -> JSONType:
        """
        Read a resource set.

        https://docs.kantarainitiative.org/uma/rec-oauth-resource-reg-v1_0_1.html#read-resource-set

        :param str token: client access token
        :param str id: Identifier of the resource set
        :rtype: dict
        """
        return self._realm.client.get(
            "{}/{}".format(self.well_known["resource_set_registration_endpoint"], id),
            headers=self.get_headers(token),
        )

    def resource_set_delete(self, token: str, id: str) -> JSONType:
        """
        Delete a resource set.

        https://docs.kantarainitiative.org/uma/rec-oauth-resource-reg-v1_0_1.html#delete-resource-set

        :param str token: client access token
        :param str id: Identifier of the resource set
        """
        return self._realm.client.delete(
            "{}/{}".format(self.well_known["resource_set_registration_endpoint"], id),
            headers=self.get_headers(token),
        )

    def resource_set_list(self, token: str, **kwargs: Any) -> JSONType:
        """
        List a resource set.

        https://docs.kantarainitiative.org/uma/rec-oauth-resource-reg-v1_0_1.html#list-resource-sets

        :param str token: client access token
        :param str name: (optional)
        :param str uri: (optional)
        :param str owner: (optional)
        :param str type: (optional)
        :param str scope: (optional)
        :rtype: list
        """
        return self._realm.client.get(
            self.well_known["resource_set_registration_endpoint"],
            headers=self.get_headers(token),
            **kwargs
        )

    @classmethod
    def get_headers(cls, token: str) -> Dict[str, Any]:
        return dict(cls.DEFAULT_HEADERS, **{"Authorization": "Bearer " + token})

    @staticmethod
    def get_payload(
        name: str, scopes: Optional[List[str]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        return dict(name=name, scopes=scopes or [], **kwargs)

    def _get_data(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return self._dumps(self.get_payload(*args, **kwargs))
