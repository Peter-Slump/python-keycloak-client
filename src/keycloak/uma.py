import json

from keycloak.well_known import KeycloakWellKnown

PATH_WELL_KNOWN = "auth/realms/{}/.well-known/uma-configuration"


class KeycloakUMA(object):

    _realm = None
    _well_known = None

    def __init__(self, realm):
        self._realm = realm

    @property
    def well_known(self):
        if self._well_known is None:
            self._well_known = KeycloakWellKnown(
                realm=self._realm,
                path=self._realm.client.get_full_url(
                    PATH_WELL_KNOWN.format(self._realm.realm_name)
                )
            )
        return self._well_known

    def resource_set_create(self, token, name, uri=None, type=None,
                            scopes=None, icon_url=None):
        """
        Create a resource set.

        https://docs.kantarainitiative.org/uma/rec-oauth-resource-reg-v1_0_1.html#rfc.section.2.2.1

        :param str token: client access token
        :param str name:
        :param str | None uri:
        :param str | None type:
        :param list | None scopes:
        :param str | none icon_url:
        :rtype: str
        """

        payload = {
            'name': name,
            'scopes': scopes or []
        }
        if uri:
            payload['uri'] = uri

        if type:
            payload['type'] = type

        if icon_url:
            payload['icon_url'] = icon_url

        return self._realm.client.post(
            self.well_known['resource_set_registration_endpoint'],
            data=json.dumps(payload),
            headers={
                "Authorization": "Bearer " + token,
                "Content-type": 'application/json'
            }
        )
