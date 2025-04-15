"""
Utility functions for the Enemera API client.
"""

from datetime import datetime, date
from typing import Union, Dict, Any, Optional
import dateutil.parser
import enum

from . import Area
from .exceptions import ValidationError
from .constants import DATE_FORMAT



def validate_date(date_str: str) -> str:
    """
    Validate that a date string is in the correct format (YYYY-MM-DD).

    Args:
        date_str: Date string to validate

    Returns:
        The validated date string

    Raises:
        ValidationError: If the date is not in the correct format
    """
    try:
        # Try to parse the date
        parsed_date = datetime.strptime(date_str, DATE_FORMAT).date()
        # Return the formatted date string
        return parsed_date.strftime(DATE_FORMAT)
    except ValueError:
        raise ValidationError(f"Invalid date format: {date_str}. Expected format: YYYY-MM-DD")


def format_date(date_obj: Union[datetime, date]) -> str:
    """
    Format a date object as a string for API requests.

    Args:
        date_obj: Date object to format

    Returns:
        Formatted date string (YYYY-MM-DD)
    """
    if isinstance(date_obj, datetime):
        return date_obj.date().strftime(DATE_FORMAT)
    else:
        return date_obj.strftime(DATE_FORMAT)


def parse_datetime(datetime_str: str) -> datetime:
    """
    Parse a datetime string from the API response.

    Args:
        datetime_str: Datetime string to parse

    Returns:
        Parsed datetime object
    """
    return dateutil.parser.parse(datetime_str)


def prepare_params(params: Dict[str, Any]) -> Dict[str, str]:
    """
    Prepare parameters for API requests by converting dates, enums, and other values.

    Args:
        params: Dictionary of parameters

    Returns:
        Processed parameters dictionary with all values as strings
    """
    processed = {}

    for key, value in params.items():
        if value is None:
            continue

        if isinstance(value, (datetime, date)):
            processed[key] = format_date(value)
        elif isinstance(value, enum.Enum):
            processed[key] = str(value)
        else:
            processed[key] = str(value)

    return processed