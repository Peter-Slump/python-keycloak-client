import asynctest

try:
    import aiohttp
except ImportError:
    aiohttp = None
else:
    from keycloak.aio.client import KeycloakClient


@asynctest.skipIf(aiohttp is None, "aiohttp is not installed")
class KeycloakClientTestCase(asynctest.TestCase):
    async def setUp(self):
        self.Session_mock_handle = asynctest.patch(
            "keycloak.aio.client.aiohttp.client.ClientSession", autospec=True
        )

        self.Session_mock = self.Session_mock_handle.start()
        self.headers = {"initial": "header"}
        self.server_url = "https://example.com"
        self.client = await KeycloakClient(
            server_url=self.server_url,
            headers=self.headers,
            session_factory=self.Session_mock,
            loop=self.loop,
        )

        self.addCleanup(self.Session_mock_handle.stop)

    async def tearDown(self):
        await self.client.close()

    def test_default_client_logger_name(self):
        """
        Case: Session get requested
        Expected: Session object get returned and the same one if called for
                  the second time
        """

        self.assertEqual(self.client.logger.name, "KeycloakClient")

    async def test_uninitialized_client(self):
        """
        Case: Session get requested
        Expected: Session object get returned and the same one if called for
                  the second time
        """
        await self.client.close()

        with self.assertRaises(RuntimeError):
            _ = self.client.session  # noqa: F841

    def test_session(self):
        """
        Case: Session get requested
        Expected: Session object get returned and the same one if called for
                  the second time
        """
        session = self.client.session
        self.assertIsInstance(session, aiohttp.ClientSession)

        self.assertEqual(session, self.client.session)

    async def test_close_session(self):
        """
        Case: Session get requested
        Expected: Session object get returned and the same one if called for
                  the second time
        """
        await self.client.close()
        with self.assertRaises(RuntimeError):
            _ = self.client.session  # noqa: F841

        self.assertIsNone(self.client._session)

    def test_get_full_url(self):
        """
        Case: retrieve a valid url
        Expected: The path get added to the base url or to the given url
        """
        self.assertEqual(
            self.client.get_full_url("/some/path"), "https://example.com/some/path"
        )

        self.assertEqual(
            self.client.get_full_url("/some/path", "https://another_url.com"),
            "https://another_url.com/some/path",
        )

    async def test_post(self):
        """
        Case: A POST request get executed
        Expected: The correct parameters get given to the request library
        """
        self.Session_mock.return_value.headers = asynctest.MagicMock()

        self.client._handle_response = asynctest.CoroutineMock()
        response = await self.client.post(
            url="https://example.com/test",
            data={"some": "data"},
            headers={"some": "header"},
            extra="param",
        )

        self.Session_mock.return_value.post.assert_called_once_with(
            "https://example.com/test",
            data={"some": "data"},
            headers={"some": "header"},
            params={"extra": "param"},
        )

        self.client._handle_response.assert_awaited_once_with(
            self.Session_mock.return_value.post.return_value
        )
        self.assertEqual(response, self.client._handle_response.return_value)

    async def test_get(self):
        """
        Case: A GET request get executed
        Expected: The correct parameters get given to the request library
        """
        self.Session_mock.return_value.headers = asynctest.CoroutineMock()

        self.client._handle_response = asynctest.CoroutineMock()
        response = await self.client.get(
            url="https://example.com/test", headers={"some": "header"}, extra="param"
        )

        self.Session_mock.return_value.get.assert_called_once_with(
            "https://example.com/test",
            headers={"some": "header"},
            params={"extra": "param"},
        )

        self.client._handle_response.assert_awaited_once_with(
            self.Session_mock.return_value.get.return_value
        )
        self.assertEqual(response, self.client._handle_response.return_value)

    async def test_put(self):
        """
        Case: A PUT request get executed
        Expected: The correct parameters get given to the request library
        """
        self.Session_mock.return_value.headers = asynctest.MagicMock()

        self.client._handle_response = asynctest.CoroutineMock()
        response = await self.client.put(
            url="https://example.com/test",
            data={"some": "data"},
            headers={"some": "header"},
            extra="param",
        )

        self.Session_mock.return_value.put.assert_called_once_with(
            "https://example.com/test",
            data={"some": "data"},
            headers={"some": "header"},
            params={"extra": "param"},
        )

        self.client._handle_response.assert_awaited_once_with(
            self.Session_mock.return_value.put.return_value
        )
        self.assertEqual(response, self.client._handle_response.return_value)

    async def test_delete(self):
        """
        Case: A DELETE request get executed
        Expected: The correct parameters get given to the request library
        """
        self.Session_mock.return_value.headers = asynctest.MagicMock()
        self.Session_mock.return_value.delete = asynctest.CoroutineMock()

        response = await self.client.delete(
            url="https://example.com/test", headers={"some": "header"}, extra="param"
        )

        self.Session_mock.return_value.delete.assert_called_once_with(
            "https://example.com/test", headers={"some": "header"}, extra="param"
        )
        self.assertEqual(response, self.Session_mock.return_value.delete.return_value)

    async def test_handle_response(self):
        """
        Case: Response get processed
        Expected: Decoded json get returned else raw_response
        """
        req_ctx = asynctest.MagicMock()
        response = req_ctx.__aenter__.return_value
        response.json = asynctest.CoroutineMock()
        response.read = asynctest.CoroutineMock()

        processed_response = await self.client._handle_response(req_ctx)

        response.raise_for_status.assert_called_once_with()
        response.json.assert_awaited_once_with(content_type=None)

        self.assertEqual(processed_response, await response.json())

        response.json.side_effect = ValueError
        processed_response = await self.client._handle_response(req_ctx)

        self.assertEqual(processed_response, await response.read())
