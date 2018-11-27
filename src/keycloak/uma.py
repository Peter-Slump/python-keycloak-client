import json

try:
    from urllib.parse import urlencode  # noqa: F401
except ImportError:
    from urllib import urlencode  # noqa: F401

from keycloak.mixins import WellKnownMixin

PATH_WELL_KNOWN = "auth/realms/{}/.well-known/uma2-configuration"


class KeycloakUMA(WellKnownMixin, object):
    DEFAULT_HEADERS = {"Content-type": 'application/json'}

    _realm = None
    _well_known = None
    _dumps = staticmethod(json.dumps)

    def __init__(self, realm):
        self._realm = realm

    def get_path_well_known(self):
        return PATH_WELL_KNOWN

    def resource_set_create(self, token, name, **kwargs):
        """
        Create a resource set.

        https://docs.kantarainitiative.org/uma/rec-oauth-resource-reg-v1_0_1.html#rfc.section.2.2.1

        :param str token: client access token
        :param str id: Identifier of the resource set
        :param str name:
        :param str uri: (optional)
        :param str type: (optional)
        :param list scopes: (optional)
        :param str icon_url: (optional)
        :param str DisplayName: (optional)
        :param boolean ownerManagedAccess: (optional)
        :param str owner: (optional)
        :rtype: str
        """
        return self._realm.client.post(
            self.well_known['resource_registration_endpoint'],
            data=self._get_data(name=name, **kwargs),
            headers=self.get_headers(token)
        )

    def resource_set_update(self, token, id, name, **kwargs):
        """
        Update a resource set.

        https://docs.kantarainitiative.org/uma/rec-oauth-resource-reg-v1_0_1.html#update-resource-set

        :param str token: client access token
        :param str id: Identifier of the resource set
        :param str name:
        :param str uri: (optional)
        :param str type: (optional)
        :param list scopes: (optional)
        :param str icon_url: (optional)
        :rtype: str
        """
        return self._realm.client.put(
            '{}/{}'.format(
                self.well_known['resource_registration_endpoint'], id),
            data=self._get_data(name=name, **kwargs),
            headers=self.get_headers(token)
        )

    def resource_set_read(self, token, id):
        """
        Read a resource set.

        https://docs.kantarainitiative.org/uma/rec-oauth-resource-reg-v1_0_1.html#read-resource-set

        :param str token: client access token
        :param str id: Identifier of the resource set
        :rtype: dict
        """
        return self._realm.client.get(
            '{}/{}'.format(
                self.well_known['resource_registration_endpoint'], id),
            headers=self.get_headers(token)
        )

    def resource_set_delete(self, token, id):
        """
        Delete a resource set.

        https://docs.kantarainitiative.org/uma/rec-oauth-resource-reg-v1_0_1.html#delete-resource-set

        :param str token: client access token
        :param str id: Identifier of the resource set
        """
        return self._realm.client.delete(
            '{}/{}'.format(
                self.well_known['resource_registration_endpoint'], id),
            headers=self.get_headers(token)
        )

    def resource_set_list(self, token, **kwargs):
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
            self.well_known['resource_registration_endpoint'],
            headers=self.get_headers(token),
            **kwargs
        )

    def resource_create_ticket(self, token, id, scopes, **kwargs):
        """
        Create a ticket form permission to resource.

        https://www.keycloak.org/docs/latest/authorization_services/index.html#_service_protection_permission_api_papi

        :param str token: user access token
        :param str id: resource id
        :param list scopes: scopes access is wanted
        :param dict claims: (optional)
        :rtype: dict
        """
        data = dict(resource_id=id, resource_scopes=scopes, **kwargs)
        return self._realm.client.post(
            self.well_known['permission_endpoint'],
            data=self._dumps([data]),
            headers=self.get_headers(token)
        )

    def resource_associate_permission(self, token, id, name, scopes, **kwargs):
        """
        Associates a permission with a Resource.

        https://www.keycloak.org/docs/latest/authorization_services/index.html#_service_authorization_uma_policy_api

        :param str token: client access token
        :param str id: resource id
        :param str name: permission name
        :param list scopes: scopes access is wanted
        :param str description:optional
        :param list roles: (optional)
        :param list groups: (optional)
        :param list clients: (optional)
        :param str condition: (optional)
        :rtype: dict
        """
        return self._realm.client.post(
            '{}/{}'.format(self.well_known['policy_endpoint'], id),
            data=self._get_data(name=name, scopes=scopes, **kwargs),
            headers=self.get_headers(token)
        )

    def permission_update(self, token, id, **kwargs):
        """
        To update an existing permission.

        https://www.keycloak.org/docs/latest/authorization_services/index.html#_service_authorization_uma_policy_api

        :param str token: client access token
        :param str id: permission id

        :rtype: dict
        """
        return self._realm.client.put(
            '{}/{}'.format(self.well_known['policy_endpoint'], id),
            data=self._dumps(kwargs),
            headers=self.get_headers(token)
        )

    def permission_delete(self, token, id):
        """
        Removing a Permission.

        https://www.keycloak.org/docs/latest/authorization_services/index.html#removing-a-permission

        :param str token: client access token
        :param str id: permission id

        :rtype: dict
        """
        return self._realm.client.delete(
            '{}/{}'.format(self.well_known['policy_endpoint'], id),
            headers=self.get_headers(token)
        )

    def permission_list(self, token, **kwargs):
        """
        Querying permission

        https://www.keycloak.org/docs/latest/authorization_services/index.html#querying-permission


        :param str token: client access token
        :param str resource: (optional)
        :param str name: (optional)
        :param str scope: (optional)

        :rtype: dict
        """
        return self._realm.client.get(
            self.well_known['policy_endpoint'],
            headers=self.get_headers(token),
            **kwargs
        )

    @classmethod
    def get_headers(cls, token):
        return dict(cls.DEFAULT_HEADERS, **{
            "Authorization": "Bearer " + token,
        })

    @staticmethod
    def get_payload(name, scopes=None, **kwargs):
        return dict(name=name, scopes=scopes or [], **kwargs)

    def _get_data(self, *args, **kwargs):
        return self._dumps(self.get_payload(*args, **kwargs))
