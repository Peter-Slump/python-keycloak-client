from keycloak.well_known import KeycloakWellKnown


class WellKnownMixin(object):

    def get_path_well_known(self):
        raise NotImplementedError()

    @property
    def well_known(self):
        if self._well_known is None:
            self._well_known = KeycloakWellKnown(
                realm=self._realm,
                path=self._realm.client.get_full_url(
                    self.get_path_well_known().format(self._realm.realm_name)
                )
            )
        return self._well_known
