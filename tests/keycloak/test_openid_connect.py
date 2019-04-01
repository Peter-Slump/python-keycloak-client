from unittest import TestCase

import mock

from keycloak.openid_connect import KeycloakOpenidConnect
from keycloak.realm import KeycloakRealm
from keycloak.well_known import KeycloakWellKnown


class KeycloakOpenidConnectTestCase(TestCase):

    def setUp(self):
        self.realm = mock.MagicMock(spec_set=KeycloakRealm)
        self.client_id = 'client-id'
        self.client_secret = 'client-secret'

        self.openid_client = KeycloakOpenidConnect(
            realm=self.realm,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.openid_client.well_known.contents = {
            'end_session_endpoint': 'https://logout',
            'jwks_uri': 'https://certs',
            'userinfo_endpoint': 'https://userinfo',
            'authorization_endpoint': 'https://authorization',
            'token_endpoint': 'https://token'
        }

    def test_well_known(self):
        """
        Case: .well-known is requested
        Expected: it's returned and the second time the same is returned
        """
        well_known = self.openid_client.well_known

        self.assertIsInstance(well_known, KeycloakWellKnown)
        self.assertEqual(well_known, self.openid_client.well_known)

    @mock.patch('keycloak.openid_connect.jwt')
    def test_decode_token(self, patched_jwt):
        self.openid_client.decode_token(token='test-token', key='test-key')
        patched_jwt.decode.assert_called_once_with('test-token', 'test-key',
                                                   algorithms=['RS256'],
                                                   audience=self.client_id)

    def test_logout(self):
        result = self.openid_client.logout(refresh_token='refresh-token')
        self.realm.client.post.assert_called_once_with(
            'https://logout',
            data={
                'refresh_token': 'refresh-token',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
        )
        self.assertEqual(result, self.realm.client.post.return_value)

    def test_certs(self):
        result = self.openid_client.certs()
        self.realm.client.get('https://certs')

        self.assertEqual(result, self.realm.client.get.return_value)

    def test_userinfo(self):
        result = self.openid_client.userinfo(token='token')
        self.realm.client.get.assert_called_once_with(
            'https://userinfo',
            headers={
                'Authorization': 'Bearer token'
            }
        )
        self.assertEqual(result, self.realm.client.get.return_value)

    def test_authorization_url(self):
        result = self.openid_client.authorization_url(
            redirect_uri='https://redirect-url',
            scope='scope other-scope',
            state='some-state'
        )
        self.assertEqual(
            result,
            'https://authorization?client_id=client-id&'
            'redirect_uri=https%3A%2F%2Fredirect-url&'
            'response_type=code&scope=scope+other-scope&state=some-state'
        )

    def test_authorization_code(self):
        response = self.openid_client.authorization_code(
            code='some-code',
            redirect_uri='https://redirect-uri'
        )
        self.realm.client.post.assert_called_once_with(
            'https://token',
            data={
                'grant_type': 'authorization_code',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': 'some-code',
                'redirect_uri': 'https://redirect-uri'
            }
        )
        self.assertEqual(response, self.realm.client.post.return_value)

    def test_client_credentials(self):
        response = self.openid_client.client_credentials(
            scope='scope another-scope'
        )
        self.realm.client.post.assert_called_once_with(
            'https://token',
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'scope another-scope'
            }
        )
        self.assertEqual(response, self.realm.client.post.return_value)

    def test_refresh_token(self):
        response = self.openid_client.refresh_token(
            refresh_token='refresh-token',
            scope='scope another-scope',
        )
        self.realm.client.post.assert_called_once_with(
            'https://token',
            data={
                'grant_type': 'refresh_token',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'scope another-scope',
                'refresh_token': 'refresh-token'
            }
        )
        self.assertEqual(response, self.realm.client.post.return_value)

    def test_token_exchange(self):
        response = self.openid_client.token_exchange(
            subject_token='some-token',
            audience='some-audience'
        )
        self.realm.client.post.assert_called_once_with(
            'https://token',
            data={
                'grant_type': 'urn:ietf:params:oauth:grant-type:token-'
                              'exchange',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'subject_token': 'some-token',
                'audience': 'some-audience'
            }
        )
        self.assertEqual(response, self.realm.client.post.return_value)
