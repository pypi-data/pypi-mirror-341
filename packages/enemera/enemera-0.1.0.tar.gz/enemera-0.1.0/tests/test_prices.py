"""
Tests for the prices API module.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from enemera.api.prices import ItalyPricesAPI
from enemera.models import Price


class TestPricesAPI(unittest.TestCase):
    """Test cases for the PricesAPI class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = MagicMock()
        self.prices_api = ItalyPricesAPI(self.client)

    def test_get_prices(self):
        """Test get method for prices."""
        # Mock client response
        mock_response = [
            {
                "utc": "2023-01-01T00:00:00Z",
                "market": "MGP",
                "zone": "NORD",
                "price": 100.5
            },
            {
                "utc": "2023-01-01T01:00:00Z",
                "market": "MGP",
                "zone": "NORD",
                "price": 102.3
            }
        ]
        self.client.request.return_value = mock_response

        # Call the method
        result = self.prices_api.get(
            market="MGP",
            date_from="2023-01-01",
            date_to="2023-01-02",
            area="NORD"
        )

        # Verify the result
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Price)
        self.assertEqual(result[0].market, "MGP")
        self.assertEqual(result[0].zone, "NORD")
        self.assertEqual(result[0].price, 100.5)

        # Verify the client was called correctly
        self.client.request.assert_called_once_with(
            "GET",
            "/italy/prices/MGP/",
            params={
                "date_from": "2023-01-01",
                "date_to": "2023-01-02",
                "area": "NORD"
            }
        )

    def test_get_prices_with_date_objects(self):
        """Test get method with datetime objects."""
        # Mock client response
        mock_response = [
            {
                "utc": "2023-01-01T00:00:00Z",
                "market": "MGP",
                "zone": "NORD",
                "price": 100.5
            }
        ]
        self.client.request.return_value = mock_response

        # Call the method with datetime objects
        date_from = datetime(2023, 1, 1)
        date_to = datetime(2023, 1, 2)

        result = self.prices_api.get(
            market="MGP",
            date_from=date_from,
            date_to=date_to,
            area="NORD"
        )

        # Verify the result
        self.assertEqual(len(result), 1)

        # Verify the client was called correctly
        self.client.request.assert_called_once_with(
            "GET",
            "/italy/prices/MGP/",
            params={
                "date_from": "2023-01-01",
                "date_to": "2023-01-02",
                "area": "NORD"
            }
        )


if __name__ == '__main__':
    unittest.main()