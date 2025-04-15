"""
API methods for the exchange volumes endpoint.
"""

from datetime import datetime, date
from typing import Optional, Union, Any

from enemera import get_endpoint
from enemera.models import ExchangeVolume
from enemera.utils import prepare_params
from enemera.enums import Market, Area
from enemera.validators import validate_and_transform_areas, validate_market, validate_purpose
from enemera.response import APIResponse


class ItalyExchangeVolumesAPI:
    """
    API methods for accessing the exchange volumes endpoint.
    """

    def __init__(self, client: Any):
        """
        Initialize the exchange volumes API.

        Args:
            client: Enemera API client instance
        """
        self.client = client

    def get(
            self,
            market: Union[str, Market],
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[Union[str, Area]] = None,
            purpose: Optional[str] = None
    ) -> APIResponse[ExchangeVolume]:
        """
        Get market exchange volumes for the specified market and zones.

        Args:
            market: Market identifier (e.g., MGP, MI1, MI2) or Market enum
            date_from: Start date (inclusive)
            date_to: End date (inclusive)
            area: Zone identifier or Area enum, or comma-separated list of zones (optional)
            purpose: Filter by purpose (e.g., SELL, BUY) (optional)

        Returns:
            APIResponse[ExchangeVolume]: Response containing ExchangeVolume objects with conversion methods

        Raises:
            ValidationError: If input validation fails
            AuthenticationError: If authentication fails
            APIError: If the API returns an error
            ConnectionError: If connection to the API fails
        """

        # Validate area if provided
        area_param = validate_and_transform_areas(area)

        # validate market
        validated_market = validate_market(market).value

        # validate purpose
        if purpose is not None:
            validated_purpose = validate_purpose(purpose).value
        else:
            validated_purpose = None

        # Format the endpoint
        endpoint = get_endpoint(data_type='it_exchange_volumes', market=validated_market)

        # Prepare parameters
        params = prepare_params({
            "date_from": date_from,
            "date_to": date_to,
            "area": area_param,
            "purpose": validated_purpose
        })

        # Make the request
        response = self.client.request("GET", endpoint, params=params)

        # Parse the response into ExchangeVolume objects and wrap in APIResponse
        volumes = [ExchangeVolume(**item) for item in response]
        return APIResponse(volumes, ExchangeVolume)