"""
API methods for the prices endpoint.
"""

from datetime import datetime, date
from typing import Union, Optional, Any

from enemera import get_endpoint
from enemera.models import IpexDemandFcs
from enemera.utils import prepare_params
from enemera.enums import  Area
from enemera.validators import validate_and_transform_areas
from enemera.response import APIResponse


class ItalyIpexDemandFcsAPI:
    """
    API methods for accessing the Ipex Demand fcs endpoint.
    """

    def __init__(self, client: Any):
        """
        Initialize the API.

        Args:
            client: Enemera API client instance
        """
        self.client = client

    def get(
            self,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[Union[str, Area]] = None
    ) -> APIResponse[IpexDemandFcs]:
        """
        Get forecasted IPEX demand for the specified period and zones .

        Args:
            date_from: Start date (inclusive)
            date_to: End date (inclusive)
            area: Zone identifier or Area enum, or comma-separated list of zones (optional)

        Returns:
            APIResponse[IpexDemandFcs]: Response containing data objects with conversion methods

        Raises:
            AreaValidationError: If the area identifier is invalid
            ValidationError: If other input validation fails
            AuthenticationError: If authentication fails
            APIError: If the API returns an error
            ConnectionError: If connection to the API fails
        """

        # Validate area if provided
        area_param = validate_and_transform_areas(area)

        # Format the endpoint
        endpoint = get_endpoint(data_type='it_ipex_demand_fcs')

        # Prepare parameters
        params = prepare_params({
            "date_from": date_from,
            "date_to": date_to,
            "area": area_param
        })

        # Make the request
        response = self.client.request("GET", endpoint, params=params)

        # Parse the response into Price objects and wrap in APIResponse
        data = [IpexDemandFcs(**item) for item in response]
        return APIResponse(data, IpexDemandFcs)