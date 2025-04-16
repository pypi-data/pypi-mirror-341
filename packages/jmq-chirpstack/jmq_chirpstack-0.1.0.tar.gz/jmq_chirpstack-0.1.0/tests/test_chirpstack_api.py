import unittest
from unittest.mock import patch, MagicMock
from jmq_chirpstack.chirpstack_api import JMQChirpstackAPI


class TestJMQChirpstackAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8080/api"
        self.api = JMQChirpstackAPI(base_url=self.base_url, api_key="fake_api_key")

    @patch("jmq_chirpstack.chirpstack_api.requests.get")
    def test_get_tenants(self, mock_get):
        expected = {'totalCount': 1, 'result': [{'id': 'tenant1', 'name': 'Tenant 1'}]}
        mock_resp = MagicMock()
        mock_resp.json.return_value = expected
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        result = self.api.get_tenants()
        self.assertEqual(result, {'total': 1, 'result': expected['result']})

    @patch("jmq_chirpstack.chirpstack_api.requests.get")
    def test_get_gateways(self, mock_get):
        tenant_id = "tenant1"
        expected = {'totalCount': 1, 'result': [{'id': 'gw1', 'name': 'Gateway 1'}]}
        mock_resp = MagicMock()
        mock_resp.json.return_value = expected
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        result = self.api.get_gateways(tenant_id)
        self.assertEqual(result, {'total': 1, 'result': expected['result']})

    @patch("jmq_chirpstack.chirpstack_api.requests.get")
    def test_get_applications(self, mock_get):
        tenant_id = "tenant1"
        expected = {'totalCount': 1, 'result': [{'id': 'app1', 'name': 'App 1'}]}
        mock_resp = MagicMock()
        mock_resp.json.return_value = expected
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        result = self.api.get_applications(tenant_id)
        self.assertEqual(result, {'total': 1, 'result': expected['result']})

    @patch("jmq_chirpstack.chirpstack_api.requests.get")
    def test_get_devices(self, mock_get):
        app_id = "app1"
        expected = {'totalCount': 1, 'result': [{'devEui': '1234', 'name': 'Device 1'}]}
        mock_resp = MagicMock()
        mock_resp.json.return_value = expected
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        result = self.api.get_devices(app_id)
        self.assertEqual(result, {'total': 1, 'result': expected['result']})

    @patch("jmq_chirpstack.chirpstack_api.requests.get")
    def test_get_device_profiles(self, mock_get):
        tenant_id = "tenant1"
        expected = {'totalCount': 1, 'result': [{'id': 'dp1', 'name': 'Profile 1'}]}
        mock_resp = MagicMock()
        mock_resp.json.return_value = expected
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        result = self.api.get_device_profiles(tenant_id)
        self.assertEqual(result, {'total': 1, 'result': expected['result']})

    @patch("jmq_chirpstack.chirpstack_api.requests.get")
    def test_get_multicast_groups(self, mock_get):
        app_id = "app1"
        expected = {'totalCount': 0, 'result': []}
        mock_resp = MagicMock()
        mock_resp.json.return_value = expected
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        result = self.api.get_multicast_groups(app_id)
        self.assertEqual(result, {'total': 0, 'result': []})

    @patch("jmq_chirpstack.chirpstack_api.requests.get")
    def test_get_users(self, mock_get):
        expected = {'totalCount': 1, 'result': [{'email': 'admin', 'isAdmin': True}]}
        mock_resp = MagicMock()
        mock_resp.json.return_value = expected
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        result = self.api.get_users()
        self.assertEqual(result, {'total': 1, 'result': expected['result']})


if __name__ == "__main__":
    unittest.main()
