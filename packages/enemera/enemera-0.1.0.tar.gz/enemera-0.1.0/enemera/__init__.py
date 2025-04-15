"""
Enemera API Client - A Python client for the Enemera energy data API.
"""

__version__ = "0.3.1"

from enemera.client import EnemeraClient
from enemera.exceptions import (
    EnemeraError,
    AuthenticationError,
    RateLimitError,
    APIError,
    ValidationError,
    ConnectionError
)
from enemera.models import Price, ExchangeVolume, CommercialFlow, BaseAPIModel
from enemera.enums import Market, Area, Purpose
from enemera.validators import (
    validate_market,
    validate_area,
    validate_enum,
    MarketValidationError,
    AreaValidationError
)
from enemera.endpoint_utils import get_endpoint
from enemera.data_utils import to_pandas, to_polars, to_csv, to_excel
from enemera.response import APIResponse

__all__ = [
    "EnemeraClient",
    "EnemeraError",
    "AuthenticationError",
    "RateLimitError",
    "APIError",
    "ValidationError",
    "ConnectionError",
    "MarketValidationError",
    "AreaValidationError",
    "Price",
    "ExchangeVolume",
    "CommercialFlow",
    "BaseAPIModel",
    "Market",
    "Area",
    "Purpose",
    "validate_market",
    "validate_area",
    "validate_enum",
    "get_endpoint",
    "to_pandas",
    "to_polars",
    "to_csv",
    "to_excel",
    "APIResponse"
]