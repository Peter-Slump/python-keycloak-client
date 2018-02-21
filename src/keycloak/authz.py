PATH_ENTITLEMENT = "auth/realms/{}/authz/entitlement/{}"


class KeycloakAuthz(object):

    _realm = None
    _client_id = None

    def __init__(self, realm, client_id):
        """

        :param keycloak.realm.KeycloakRealm realm:
        :param client_id:
        """
        self._realm = realm
        self._client_id = client_id

    def entitlement(self, token):
        """
        Client applications can use a specific endpoint to obtain a special
        security token called a requesting party token (RPT). This token
        consists of all the entitlements (or permissions) for a user as a
        result of the evaluation of the permissions and authorization policies
        associated with the resources being requested. With an RPT, client
        applications can gain access to protected resources at the resource
        server.

        http://www.keycloak.org/docs/latest/authorization_services/index.html#_service_entitlement_api

        :rtype: dict
        """
        headers = {"Authorization": "Bearer " + token}

        return self._realm.client.get(
            self._realm.client.get_full_url(PATH_ENTITLEMENT.format(
                self._realm.realm_name, self._client_id)),
            headers=headers)
