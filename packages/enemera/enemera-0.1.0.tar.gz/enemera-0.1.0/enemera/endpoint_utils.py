"""
Utilities for working with API endpoints.
"""

from typing import Literal


def get_endpoint(
        data_type: Literal["it_prices", "it_exchange_volumes", "it_commercial_flows"],
        **kwargs
) -> str:
    """
    Generate the appropriate API endpoint based on data type and parameters.

    Args:
        data_type: Type of data to fetch (prices, exchange_volumes, commercial_flows)
        **kwargs: Parameters for endpoint construction including:
            - market: Market identifier (e.g., MGP, MI1) or Market enum
            - date_from: Start date (not used for endpoint construction)
            - date_to: End date (not used for endpoint construction)
            - area: Zone identifier or Area enum (not used for endpoint construction yet)
            - zone_from: Source zone for commercial flows (not used for endpoint construction)
            - zone_to: Destination zone for commercial flows (not used for endpoint construction)
            - purpose: Filter purpose for exchange volumes (not used for endpoint construction)

    Returns:
        str: Formatted API endpoint

    Raises:
        ValueError: If data_type is invalid or required parameters are missing
    """
    market = kwargs.get('market')

    if data_type == "it_prices":
        if market is None:
            raise ValueError(f"Market parameter is required for {data_type} endpoint")
        return f"/italy/prices/{market}/"
    elif data_type == "it_exchange_volumes":
        if market is None:
            raise ValueError(f"Market parameter is required for {data_type} endpoint")
        return f"/italy/exchange_volumes/{market}/"
    elif data_type == "it_commercial_flows":
        if market is None:
            raise ValueError(f"Market parameter is required for {data_type} endpoint")
        return f"/italy/commercial_flows/{market}"
    elif data_type == "it_ancillary_services":
        if market is None:
            raise ValueError(f"Market parameter is required for {data_type} endpoint")
        return f"/italy/ancillary_services/{market}/"
    elif data_type == "it_ipex_demand_fcs":
        return "/italy/ipex_demand/fcs/"
    elif data_type == "it_ipex_demand_act":
        return "/italy/ipex_demand/act/"

    else:
        raise ValueError(f"Invalid data_type: {data_type}")