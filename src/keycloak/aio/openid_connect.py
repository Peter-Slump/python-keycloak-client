from keycloak.aio.mixins import WellKnownMixin
from keycloak.openid_connect import (
    KeycloakOpenidConnect as SyncKeycloakOpenidConnect,
    PATH_WELL_KNOWN,
)

__all__ = (
    'KeycloakOpenidConnect',
)


class KeycloakOpenidConnect(WellKnownMixin, SyncKeycloakOpenidConnect):
    def get_path_well_known(self):
        return PATH_WELL_KNOWN

    def _token_request(self, grant_type, **kwargs):
        """
        Do the actual call to the token end-point.

        :param grant_type:
        :param kwargs: See invoking methods.
        :return:
        """
        payload = {
            'grant_type': grant_type,
            'client_id': self._client_id,
            'client_secret': self._client_secret
        }

        payload.update(**kwargs)

        return self._realm.client.post(self.get_url('token_endpoint'),
                                       data=payload)
