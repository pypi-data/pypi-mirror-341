"""
Tests for the Enemera API client.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from enemera import EnemeraClient
from enemera.exceptions import AuthenticationError, APIError, RateLimitError


class TestEnemeraClient(unittest.TestCase):
    """Test cases for the EnemeraClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_api_key"
        self.client = EnemeraClient(api_key=self.api_key)

    def test_initialization(self):
        """Test client initialization."""
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertIn("Authorization", self.client.session.headers)
        self.assertEqual(
            self.client.session.headers["Authorization"],
            f"Bearer {self.api_key}"
        )

    @patch('requests.Session.request')
    def test_request_success(self, mock_request):
        """Test successful request."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test_data"}
        mock_response.content = True
        mock_request.return_value = mock_response

        # Make request
        result = self.client.request("GET", "/test/endpoint")

        # Verify result
        self.assertEqual(result, {"data": "test_data"})
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_authentication_error(self, mock_request):
        """Test authentication error handling."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_request.return_value = mock_response

        # Check that the appropriate exception is raised
        with self.assertRaises(AuthenticationError):
            self.client.request("GET", "/test/endpoint")

    @patch('requests.Session.request')
    def test_rate_limit_error(self, mock_request):
        """Test rate limit error handling."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_request.return_value = mock_response

        # Check that the appropriate exception is raised
        with self.assertRaises(RateLimitError):
            self.client.request("GET", "/test/endpoint")

    @patch('requests.Session.request')
    def test_api_error(self, mock_request):
        """Test API error handling."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Bad request"}
        mock_request.return_value = mock_response

        # Check that the appropriate exception is raised
        with self.assertRaises(APIError) as context:
            self.client.request("GET", "/test/endpoint")

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Bad request")


if __name__ == '__main__':
    unittest.main()