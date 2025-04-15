"""
Utility functions for data format conversion in the Enemera API client.
"""

import pathlib
from datetime import datetime
from typing import List, TypeVar, Union, Optional

# Type variable for any model with to_dict method
T = TypeVar('T')


def to_pandas(data: List[T], index_col: Optional[str] = None) -> 'pandas.DataFrame':
    """
    Convert a list of Pydantic models to a pandas DataFrame.

    Args:
        data: List of Pydantic model instances
        index_col: Column to use as index (optional)

    Returns:
        pandas.DataFrame: Pandas DataFrame representing the data

    Raises:
        ImportError: If pandas is not installed
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "Pandas is required for this functionality. "
            "Install it with `pip install pandas`"
        )

    if not data:
        return pd.DataFrame()

    # Convert each model to a dict
    dict_data = [item.dict() for item in data]

    # Create DataFrame
    df = pd.DataFrame(dict_data)

    # Set index if specified
    if index_col and index_col in df.columns:
        df.set_index(index_col, inplace=True)

    # Handle datetime columns
    for col in df.columns:
        if df[col].dtype == 'object':
            # Try to convert to datetime if all elements look like dates
            if all(isinstance(x, datetime) for x in df[col] if x is not None):
                df[col] = pd.to_datetime(df[col])

    return df


def to_polars(data: List[T], index_col: Optional[str] = None) -> 'polars.DataFrame':
    """
    Convert a list of Pydantic models to a polars DataFrame.

    Args:
        data: List of Pydantic model instances
        index_col: Column to use as index (not used in polars, kept for API consistency)

    Returns:
        polars.DataFrame: Polars DataFrame representing the data

    Raises:
        ImportError: If polars is not installed
    """
    try:
        import polars as pl
    except ImportError:
        raise ImportError(
            "Polars is required for this functionality. "
            "Install it with `pip install polars`"
        )

    if not data:
        return pl.DataFrame()

    # Convert each model to a dict
    dict_data = [item.dict() for item in data]

    # Create DataFrame
    df = pl.DataFrame(dict_data)

    # Handle datetime columns - polars auto-detects them,
    # but if there are issues we could add specific handling here

    return df


def to_csv(
        data: List[T],
        filepath: Union[str, pathlib.Path],
        index_col: Optional[str] = None,
        **csv_kwargs
) -> None:
    """
    Save a list of Pydantic models to a CSV file.

    Args:
        data: List of Pydantic model instances
        filepath: Path to save the CSV file
        index_col: Column to use as index (not used, kept for API consistency)
        **csv_kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_csv

    Raises:
        ImportError: If pandas is not installed
    """
    df = to_pandas(data)

    try:
        df.to_csv(filepath, **csv_kwargs)
    except Exception as e:
        raise ValueError(f"Failed to save data to CSV: {str(e)}")


def to_excel(
        data: List[T],
        filepath: Union[str, pathlib.Path],
        sheet_name: str = "Sheet1",
        index_col: Optional[str] = None,
        engine: str = "openpyxl",
        **excel_kwargs
) -> None:
    """
    Save a list of Pydantic models to an Excel file.

    Args:
        data: List of Pydantic model instances
        filepath: Path to save the Excel file
        sheet_name: Name of the sheet to save the data to
        index_col: Column to use as index (optional)
        engine: Excel engine to use (default: openpyxl)
        **excel_kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_excel

    Raises:
        ImportError: If pandas or an Excel engine is not installed
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "Pandas is required for this functionality. "
            "Install it with `pip install pandas`"
        )

    # Get pandas DataFrame
    df = to_pandas(data, index_col=index_col)

    # Check if engine is available
    if engine == "openpyxl":
        try:
            import openpyxl
        except ImportError:
            raise ImportError(
                "Openpyxl is required for Excel export with the openpyxl engine. "
                "Install it with `pip install openpyxl`"
            )
    elif engine == "xlsxwriter":
        try:
            import xlsxwriter
        except ImportError:
            raise ImportError(
                "XlsxWriter is required for Excel export with the xlsxwriter engine. "
                "Install it with `pip install xlsxwriter`"
            )

    # Save to Excel
    try:
        df.to_excel(
            filepath,
            sheet_name=sheet_name,
            engine=engine,
            **excel_kwargs
        )
    except Exception as e:
        raise ValueError(f"Failed to save data to Excel: {str(e)}")