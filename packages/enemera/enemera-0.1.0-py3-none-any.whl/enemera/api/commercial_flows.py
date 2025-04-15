"""
API methods for the commercial flows endpoint.
"""

from datetime import datetime, date
from typing import Optional, Union, Any

from enemera import get_endpoint, validate_market
from enemera.models import CommercialFlow
from enemera.utils import prepare_params
from enemera.enums import Market, Area
from enemera.validators import validate_and_transform_areas
from enemera.response import APIResponse


class ItalyCommercialFlowsAPI:
    """
    API methods for accessing the commercial flows endpoint.
    """

    def __init__(self, client: Any):
        """
        Initialize the commercial flows API.

        Args:
            client: Enemera API client instance
        """
        self.client = client

    def get(
            self,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            market: Optional[Union[str, Market]] = None,
            zone_from: Optional[Union[str, Area]] = None,
            zone_to: Optional[Union[str, Area]] = None
    ) -> APIResponse[CommercialFlow]:
        """
        Get commercial electricity flows between zones.

        Args:
            date_from: Start date (inclusive)
            date_to: End date (inclusive)
            market: Market identifier (e.g., MGP, MI1) or Market enum (optional)
            zone_from: Source zone identifier or Area enum (optional)
            zone_to: Destination zone identifier or Area enum (optional)

        Returns:
            APIResponse[CommercialFlow]: Response containing CommercialFlow objects with conversion methods

        Raises:
            ValidationError: If input validation fails
            AuthenticationError: If authentication fails
            APIError: If the API returns an error
            ConnectionError: If connection to the API fails
        """

        # validate market
        validated_market = validate_market(market).value

        # Format the endpoint
        endpoint = get_endpoint(data_type='it_commercial_flows', market=validated_market)

        # Validate area if provided
        area_from_param = validate_and_transform_areas(zone_from)
        area_to_param = validate_and_transform_areas(zone_to)

        # Prepare parameters
        params = prepare_params({
            "date_from": date_from,
            "date_to": date_to,
            "market": validated_market,
            "zone_from": area_from_param,
            "zone_to": area_to_param
        })

        # Make the request
        response = self.client.request("GET", endpoint, params=params)

        # Parse the response into CommercialFlow objects and wrap in APIResponse
        flows = [CommercialFlow(**item) for item in response]
        return APIResponse(flows, CommercialFlow)