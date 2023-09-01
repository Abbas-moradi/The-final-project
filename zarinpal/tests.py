import unittest
from unittest.mock import patch, MagicMock
from .views import send_request, verify
import requests.exceptions


class TestZarinPalAPI(unittest.TestCase):

    @patch('requests.post')
    def test_send_request_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'Status': 100,
            'Authority': '123456789'
        }
        mock_post.return_value = mock_response

        result = send_request('YOUR_TEST_AUTHORITY')
        self.assertTrue(result['status'])
        self.assertEqual(result['authority'], '123456789')

    @patch('requests.post')
    def test_send_request_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'Status': 101
        }
        mock_post.return_value = mock_response

        result = send_request('YOUR_TEST_AUTHORITY')
        self.assertFalse(result['status'])
        self.assertEqual(result['code'], '101')

    @patch('requests.post')
    def test_send_request_timeout(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout

        result = send_request('YOUR_TEST_AUTHORITY')
        self.assertFalse(result['status'])
        self.assertEqual(result['code'], 'timeout')

    @patch('requests.post')
    def test_send_request_connection_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError

        result = send_request('YOUR_TEST_AUTHORITY')
        self.assertFalse(result['status'])
        self.assertEqual(result['code'], 'connection error')

    @patch('requests.post')
    def test_verify_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'Status': 100,
            'RefID': '123456'
        }
        mock_post.return_value = mock_response

        result = verify('YOUR_TEST_AUTHORITY')
        self.assertTrue(result['status'])
        self.assertEqual(result['RefID'], '123456')

    @patch('requests.post')
    def test_verify_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'Status': 101
        }
        mock_post.return_value = mock_response

        result = verify('YOUR_TEST_AUTHORITY')
        self.assertFalse(result['status'])
        self.assertEqual(result['code'], '101')

if __name__ == '__main__':
    unittest.main()
