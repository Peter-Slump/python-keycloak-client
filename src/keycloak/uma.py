import json

from keycloak.mixins import WellKnownMixin

PATH_WELL_KNOWN = "auth/realms/{}/.well-known/uma-configuration"


class KeycloakUMA(WellKnownMixin, object):

    _realm = None
    _well_known = None

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
        :rtype: str
        """
        return self._realm.client.post(
            self.well_known['resource_set_registration_endpoint'],
            data=json.dumps(
                self.get_payload(name=name, **kwargs)
            ),
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
                self.well_known['resource_set_registration_endpoint'], id),
            data=json.dumps(
                self.get_payload(name=name, **kwargs)
            ),
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
                self.well_known['resource_set_registration_endpoint'], id),
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
                self.well_known['resource_set_registration_endpoint'], id),
            headers=self.get_headers(token)
        )

    def resource_set_list(self, token):
        """
        List a resource set.

        https://docs.kantarainitiative.org/uma/rec-oauth-resource-reg-v1_0_1.html#list-resource-sets

        :param str token: client access token
        :rtype: list
        """
        return self._realm.client.get(
            self.well_known['resource_set_registration_endpoint'],
            headers=self.get_headers(token)
        )

    def get_headers(self, token):
        return {
            "Authorization": "Bearer " + token,
            "Content-type": 'application/json'
        }

    def get_payload(self, name, scopes=None, **kwargs):
        payload = {
            'name': name,
            'scopes': scopes or []
        }
        payload.update(**kwargs)

        return payload
