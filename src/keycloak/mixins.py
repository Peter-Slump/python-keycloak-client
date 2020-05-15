from typing import Optional

from keycloak import realm
from keycloak import well_known


class WellKnownMixin:
    _well_known: Optional["well_known.KeycloakWellKnown"] = None
    _realm: Optional["realm.KeycloakRealm"] = None

    def get_path_well_known(self):
        raise NotImplementedError()

    @property
    def well_known(self) -> "well_known.KeycloakWellKnown":
        if self._well_known is None:
            self._well_known = well_known.KeycloakWellKnown(
                client=self._realm.client,
                path=self._realm.client.get_full_url(
                    self.get_path_well_known().format(self._realm.realm_name)
                ),
            )
        return self._well_known
