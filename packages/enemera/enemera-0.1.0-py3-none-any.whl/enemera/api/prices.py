"""
API methods for the prices endpoint.
"""

from datetime import datetime, date
from typing import Union, Optional, Any

from enemera import get_endpoint
from enemera.models import Price
from enemera.utils import prepare_params
from enemera.enums import Market, Area
from enemera.validators import validate_and_transform_areas, validate_market
from enemera.response import APIResponse


class ItalyPricesAPI:
    """
    API methods for accessing the prices endpoint.
    """

    def __init__(self, client: Any):
        """
        Initialize the prices API.

        Args:
            client: Enemera API client instance
        """
        self.client = client

    def get(
            self,
            market: Union[str, Market],
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[Union[str, Area]] = None
    ) -> APIResponse[Price]:
        """
        Get market prices for the specified market and zones.

        Args:
            market: Market identifier (e.g., MGP, MI1, MI2) or Market enum
            date_from: Start date (inclusive)
            date_to: End date (inclusive)
            area: Zone identifier or Area enum, or comma-separated list of zones (optional)

        Returns:
            APIResponse[Price]: Response containing Price objects with conversion methods

        Raises:
            MarketValidationError: If the market identifier is invalid
            AreaValidationError: If the area identifier is invalid
            ValidationError: If other input validation fails
            AuthenticationError: If authentication fails
            APIError: If the API returns an error
            ConnectionError: If connection to the API fails
        """

        # Validate area if provided
        area_param = validate_and_transform_areas(area)

        # validate market
        validated_market = validate_market(market).value

        # Format the endpoint
        endpoint = get_endpoint(data_type='it_prices', market=validated_market)

        # Prepare parameters
        params = prepare_params({
            "date_from": date_from,
            "date_to": date_to,
            "area": area_param
        })

        # Make the request
        response = self.client.request("GET", endpoint, params=params)

        # Parse the response into Price objects and wrap in APIResponse
        prices = [Price(**item) for item in response]
        return APIResponse(prices, Price)