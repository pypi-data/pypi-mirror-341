"""
Data models for the Enemera API client responses.
"""

from datetime import datetime
from typing import List, Optional, Union, TypeVar, ClassVar, Type
import pathlib
from pydantic import BaseModel, Field

from .data_utils import to_pandas, to_polars, to_csv, to_excel

# Type variable for self-reference in class methods
T = TypeVar('T', bound='BaseAPIModel')


class BaseAPIModel(BaseModel):
    """
    Base model class with common conversion methods.
    """

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

    @classmethod
    def to_pandas(cls: Type[T], data: List[T], index_col: Optional[str] = None):
        """
        Convert a list of model instances to a pandas DataFrame.

        Args:
            data: List of model instances
            index_col: Column to use as index (optional)

        Returns:
            pandas.DataFrame: Pandas DataFrame representing the data
        """
        return to_pandas(data, index_col=index_col)

    @classmethod
    def to_polars(cls: Type[T], data: List[T], index_col: Optional[str] = None):
        """
        Convert a list of model instances to a polars DataFrame.

        Args:
            data: List of model instances
            index_col: Column to use as index (not used in polars, kept for API consistency)

        Returns:
            polars.DataFrame: Polars DataFrame representing the data
        """
        return to_polars(data, index_col=index_col)

    @classmethod
    def to_csv(
            cls: Type[T],
            data: List[T],
            filepath: Union[str, pathlib.Path],
            index_col: Optional[str] = None,
            **csv_kwargs
    ):
        """
        Save a list of model instances to a CSV file.

        Args:
            data: List of model instances
            filepath: Path to save the CSV file
            index_col: Column to use as index (optional)
            **csv_kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_csv
        """
        to_csv(data, filepath, index_col=index_col, **csv_kwargs)

    @classmethod
    def to_excel(
            cls: Type[T],
            data: List[T],
            filepath: Union[str, pathlib.Path],
            sheet_name: str = "Sheet1",
            index_col: Optional[str] = None,
            engine: str = "openpyxl",
            **excel_kwargs
    ):
        """
        Save a list of model instances to an Excel file.

        Args:
            data: List of model instances
            filepath: Path to save the Excel file
            sheet_name: Name of the sheet to save the data to
            index_col: Column to use as index (optional)
            engine: Excel engine to use (default: openpyxl)
            **excel_kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_excel
        """
        to_excel(
            data,
            filepath,
            sheet_name=sheet_name,
            index_col=index_col,
            engine=engine,
            **excel_kwargs
        )


class Price(BaseAPIModel):
    """
    Model representing a price data point from the API.
    """
    utc: datetime = Field(..., description="UTC timestamp of the data point")
    market: str = Field(..., description="Market identifier (e.g., MGP, MI1, MI2)")
    zone: str = Field(..., description="Zone identifier")
    price: float = Field(..., description="Price value in EUR/MWh")


class ExchangeVolume(BaseAPIModel):
    """
    Model representing a market volume data point from the API.
    """
    utc: datetime = Field(..., description="UTC timestamp of the data point")
    market: str = Field(..., description="Market identifier (e.g., MGP, MI1, MI2)")
    zone: str = Field(..., description="Zone identifier")
    purpose: str = Field(..., description="Purpose (e.g., SELL, BUY)")
    quantity: float = Field(..., description="Quantity value in MW")


class CommercialFlow(BaseAPIModel):
    """
    Model representing a commercial electricity flow data point from the API.
    """
    utc: datetime = Field(..., description="UTC timestamp of the data point")
    market: str = Field(..., description="Market identifier (e.g., MGP, MI1)")
    zone_from: str = Field(..., description="Source zone identifier")
    zone_to: str = Field(..., description="Destination zone identifier")
    flow_MW: float = Field(..., description="Flow value in MW")

class AncillaryServices(BaseAPIModel):
    """
    Model representing ancillary services data point from the API.
    """
    utc: datetime = Field(..., description="UTC timestamp of the data point")
    #market: str = Field(..., description="Market identifier (e.g., MSD, MB)")
    market_segment: str = Field(..., description="Market segment identifier (e.g., MSD, MB, MBs, MBa)")
    zone: str = Field(..., description="Zone identifier")
    buy_vol_rev: Optional[float] = Field(None, description="Buy volume with revision")
    sell_vol_rev: Optional[float] = Field(None, description="Sell volume with revision")
    buy_vol_norev: Optional[float] = Field(None, description="Buy volume without revision")
    sell_vol_norev: Optional[float] = Field(None, description="Sell volume without revision")
    avg_buy_price: Optional[float] = Field(None, description="Average buy price")
    avg_sell_price: Optional[float] = Field(None, description="Average sell price")
    max_sell_price: Optional[float] = Field(None, description="Maximum sell price")
    min_buy_price: Optional[float] = Field(None, description="Minimum buy price")

class IpexDemandFcs(BaseAPIModel):
    """
    Model representing an IPEX demand fcs data point from the API.
    """
    utc: datetime = Field(..., description="UTC timestamp of the data point")
    zone: str = Field(..., description="Zone identifier")
    demand: float = Field(..., description="Demand value in MW")

class IpexDemandAct(BaseAPIModel):
    """
    Model representing an IPEX actual demand data point from the API.
    """
    utc: datetime = Field(..., description="UTC timestamp of the data point")
    zone: str = Field(..., description="Zone identifier")
    demand: float = Field(..., description="Demand value in MW")
